import base64
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .models import AttendanceLog

def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('field_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'fieldguard/login.html', {'form': form})


@login_required
def field_dashboard(request):
    logs = AttendanceLog.objects.filter(staff=request.user).order_by('-timestamp')[:5]
    return render(request, 'fieldguard/dashboard.html', {'logs': logs})


@login_required
def process_checkin(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        county = request.POST.get('county')
        image_data = request.POST.get('image')

        if not all([lat, lng, county, image_data]):
            return JsonResponse({'status': 'error', 'message': 'Missing data packages.'}, status=400)

        try:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"site_{request.user.username}_{county}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=file_name)

            log = AttendanceLog(
                staff=request.user,
                latitude=lat,
                longitude=lng,
                assigned_county=county,
                field_photo=data
            )
            log.save()

            success, message = log.verify_location()
            log.is_location_valid = success
            log.verification_message = message
            log.save()

            return JsonResponse({'status': 'success' if success else 'failed', 'message': message})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method unauthorized.'}, status=405)


def staff_logout(request):
    logout(request)
    return redirect('staff_login')