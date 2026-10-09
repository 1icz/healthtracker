import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Measurement
from .forms import MeasurementForm, RegisterForm, ProfileForm


@login_required
def index(request):
    measurements = Measurement.objects.filter(user=request.user).order_by('-date')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_day = request.GET.get('day')

    if start_date:
        measurements = measurements.filter(date__gte=start_date)
    if end_date:
        measurements = measurements.filter(date__lte=end_date)
    if selected_day:
        measurements = measurements.filter(date=selected_day)

    if selected_day:
        latest = measurements.first()
    else:
        latest = measurements.first()

    context = {
        'measurements': measurements,
        'latest': latest,
        'start_date': start_date,
        'end_date': end_date,
        'selected_day': selected_day,
    }
    return render(request, 'tracker/index.html', context)


@login_required
def add_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            messages.success(request, 'Измерение успешно добавлено.')
            return redirect('index')
    else:
        form = MeasurementForm()
    return render(request, 'tracker/form.html', {'form': form, 'title': 'Добавить измерение'})


@login_required
def edit_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Измерение успешно обновлено.')
            return redirect('index')
    else:
        form = MeasurementForm(instance=measurement)
    return render(request, 'tracker/form.html', {'form': form, 'title': 'Редактировать измерение'})


@login_required
def delete_measurement(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk, user=request.user)
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Измерение удалено.')
        return redirect('index')
    return render(request, 'tracker/confirm_delete.html', {'measurement': measurement})


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="measurements.csv"'

    writer = csv.writer(response)
    writer.writerow(['Дата', 'Верхнее', 'Нижнее', 'Пульс', 'Заметка'])

    measurements = Measurement.objects.filter(user=request.user).order_by('-date')
    for m in measurements:
        writer.writerow([m.date, m.systolic, m.diastolic, m.pulse, m.note])

    return response


@login_required
def chart_data(request):
    period = request.GET.get('period', 'days')
    measurements = Measurement.objects.filter(user=request.user).order_by('date')

    data = {
        'labels': [],
        'pulse': [],
        'systolic': [],
        'diastolic': []
    }

    for m in measurements:
        if period == 'days':
            label = m.date.strftime('%d.%m.%Y')
        elif period == 'months':
            label = m.date.strftime('%m.%Y')
        else:
            label = m.date.strftime('%Y')

        data['labels'].append(label)
        data['pulse'].append(m.pulse)
        data['systolic'].append(m.systolic)
        data['diastolic'].append(m.diastolic)

    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'tracker/profile.html', {'form': form})