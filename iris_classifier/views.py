from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
import csv, io
from django.http import HttpResponse
from .models import Iris, Collector
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from rest_framework import viewsets
from .serializers import IrisSerializer

import numpy as np

# --- ANA SAYFA VE LİSTELEME (READ)
def home_view(request):
    irises = Iris.objects.all()
    return render(request, 'iris_list.html', {'irises': irises})

# --- CRUD İŞLEMLERİ ---
@login_required
def iris_create(request):
    if request.method == "POST":
        # Mevcut kullanıcı için Collector profilini al veya oluştur
        collector, created = Collector.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': request.user.first_name or request.user.username,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'field_of_expertise': 'General' # Varsayılan uzmanlık alanı
            }
        )

        Iris.objects.create(
            sepal_length=request.POST['sepal_length'],
            sepal_width=request.POST['sepal_width'],
            petal_length=request.POST['petal_length'],
            petal_width=request.POST['petal_width'],
            species=request.POST['species'],
            collector=collector
        )
        return redirect('home')
    return render(request, 'iris_create.html')

@login_required
def iris_update(request, pk):
    iris = get_object_or_404(Iris, pk=pk)
    if request.method == "POST":
        iris.sepal_length = request.POST['sepal_length']
        iris.sepal_width = request.POST['sepal_width']
        iris.petal_length = request.POST['petal_length']
        iris.petal_width = request.POST['petal_width']
        iris.species = request.POST['species']
        iris.save()
        return redirect('home')
    return render(request, 'iris_update.html', {'iris': iris})

@login_required
def iris_delete(request, pk):
    iris = get_object_or_404(Iris, pk=pk)
    if request.method == "POST":
        iris.delete()
        return redirect('home')
    return render(request, 'iris_delete.html', {'iris': iris})

# --- CSV İÇE AKTARMA (IMPORT) ---
@login_required
def import_iris_csv(request):
    if request.method == "POST":
        if not request.user.has_perm('iris_classifier.add_iris'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        
        if request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            next(io_string) # Başlık satırını atla
            for row in csv.reader(io_string, delimiter=','):
                _, created = Iris.objects.update_or_create(
                    sepal_length=row[0], sepal_width=row[1],
                    petal_length=row[2], petal_width=row[3], species=row[4]
                )
            return redirect('home')
    return render(request, 'import_export.html')



# Kayıt Olma Görünümü
from .forms import CustomUserCreationForm

# Kayıt Olma Görünümü
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Kullanıcıyı otomatik olarak 'Reader' grubuna ekle [cite: 160]
            group = Group.objects.get(name='Reader')
            user.groups.add(group)
            login(request, user)
            return redirect('home') # Ana sayfaya yönlendir
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Giriş Yapma Görünümü [cite: 158]
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Çıkış Yapma Görünümü [cite: 158]
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')



def iris_search(request):
    # Veri setini baştan tümü olarak alıyoruz
    results = Iris.objects.all()
    
    # Kullanıcıdan gelen kriterleri yakalıyoruz
    species_query = request.GET.get('species')
    min_sepal_length = request.GET.get('sepal_length')
    min_sepal_width = request.GET.get('sepal_width')
    min_petal_length = request.GET.get('petal_length')
    min_petal_width = request.GET.get('petal_width')

    # Eğer kriterler girilmişse, sonuçları filtreliyoruz
    if species_query:
        results = results.filter(species__icontains=species_query)
    if min_sepal_length:
        results = results.filter(sepal_length__gte=min_sepal_length)
    if min_sepal_width:
        results = results.filter(sepal_width__gte=min_sepal_width)
    if min_petal_length:
        results = results.filter(petal_length__gte=min_petal_length)
    if min_petal_width:
        results = results.filter(petal_width__gte=min_petal_width)

    return render(request, 'search.html', {'results': results})

def export_iris_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species'])
    
    # Veri tabanındaki tüm kayıtları döngüye alarak yazdırıyoruz [cite: 169]
    for iris in Iris.objects.all():
        writer.writerow([iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width, iris.species])
        
    return response


def predict_view(request):

    prediction = None
    selected_algo = ""

    if request.method == 'POST':
        try:
            # .get() kullanırken tırnak içindeki isimler HTML'deki name ile aynı olmalı!
            sl = request.POST.get('sepal_length')
            sw = request.POST.get('sepal_width')
            pl = request.POST.get('petal_length')
            pw = request.POST.get('petal_width')
            algo = request.POST.get('algorithm')

            # Eğer verilerden biri bile gelmediyse hata mesajı göster
            if None in [sl, sw, pl, pw]:
                prediction = "Error: Some data is missing!"
            else:
                # Hepsi tamamsa float'a çevir
                sl, sw, pl, pw = float(sl), float(sw), float(pl), float(pw)

            # Scikit-learn'ün içindeki hazır 150 verilik seti yüklüyoruz
            # Bu set sayesinde veritabanına ihtiyacımız kalmıyor
            iris = load_iris()
            X = iris.data  # 150 çiçeğin ölçümleri
            y = iris.target # Bu çiçeklerin türleri (0, 1, 2 olarak)

            # Kullanıcının seçtiği algoritmayı hazırlıyoruz
            if selected_algo == 'knn':
                model = KNeighborsClassifier(n_neighbors=5)
            elif selected_algo == 'dt':
                model = DecisionTreeClassifier()
            else:
                model = SVC()

            # 4. Modeli hazır veriyle eğitiyoruz
            model.fit(X, y)

            # 5. Tahmin yapıyoruz
            res = model.predict([[sl, sw, pl, pw]])
            
            # 6. Sayısal sonucu (0,1,2) isimlere çeviriyoruz (Setosa, vb.)
            prediction = iris.target_names[res[0]].capitalize()
            
        except Exception as e:
            prediction = f"Error occurred: {e}"
            
    return render(request, 'predict.html', {'prediction': prediction})


class IrisViewSet(viewsets.ModelViewSet):
    queryset = Iris.objects.all()
    serializer_class = IrisSerializer