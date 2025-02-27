from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from .models import Holiday, AcademicCalendar
from .forms import HolidayForm, AcademicCalendarForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'district/holiday_list.html', {'holidays': holidays})

#---------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_holidays(request):
    # Create a formset factory for the Holiday model
    HolidayFormSet = modelformset_factory(Holiday, form=HolidayForm, extra=3)  # 'extra' determines additional empty forms
    
    if request.method == "POST":
        formset = HolidayFormSet(request.POST)
        if formset.is_valid():
            formset.save()  # Save all valid forms in the formset
            return redirect('holiday_list')
    else:
        formset = HolidayFormSet(queryset=Holiday.objects.none())  # Start with no pre-filled data

    return render(request, 'district/create_holidays.html', {'formset': formset})

#----------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def holiday_update(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == "POST":
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm(instance=holiday)
    return render(request, 'district/update_holiday.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def academic_calendar_detail(request):
    calendars = AcademicCalendar.objects.all()
    return render(request, 'district/academic_calendar_detail.html', {'calendars': calendars})

#-------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_academic_calendar(request):
    # Check if an AcademicCalendar instance already exists
    existing_calendar = AcademicCalendar.objects.first()
    
    if existing_calendar:
        # If a calendar exists, redirect to update view
        return redirect('academic_calendar_update', pk=existing_calendar.pk)
    
    if request.method == "POST":
        form = AcademicCalendarForm(request.POST)
        if form.is_valid():
            academic_calendar = form.save()  # Save the form data
            messages.success(request, 'Academic calendar created successfully!')
            # Example of a more specific redirect (if you have a calendar detail view)
            return redirect('academic_calendar_detail')
        else:
            return render(request, 'district/create_academic_calendar.html', {'form': form})
    else:
        form = AcademicCalendarForm()
    return render(request, 'district/create_academic_calendar.html', {'form': form})
#------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def academic_calendar_update(request, pk):
    calendar = get_object_or_404(AcademicCalendar, pk=pk)
    if request.method == "POST":
        form = AcademicCalendarForm(request.POST, instance=calendar)
        if form.is_valid():
            form.save()
            return redirect('academic_calendar_detail')
    else:
        form = AcademicCalendarForm(instance=calendar)
    return render(request, 'district/create_academic_calendar.html', {'form': form})

#--------------------------------------------

