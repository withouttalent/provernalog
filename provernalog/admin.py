from django.contrib import admin
from provernalog.models import *
from django.db.models import Sum, Count, Avg, Min, Max, F, Q
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from async_parser.tasks import convert_excel_email
from openpyxl.writer.excel import save_virtual_workbook
from user_profile.forms import ParcelFilter
from django.urls import path
from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from async_parser.models import ParserTask


class EvaluativeFactorInline(admin.TabularInline):
    model = EvaluativeFactor.parcel.through
    extra = 0
    verbose_name = "Ценообразующий фактор"
    verbose_name_plural = "Ценообразующие факторы"


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)



class SubGroupInline(admin.TabularInline):
    model = SubgroupAppraise
    extra = 0
    verbose_name = "Подгруппа"
    verbose_name_plural = "Подгруппы"


class GroupAppraiseInline(admin.TabularInline):
    model = GroupAppraise
    extra = 0


class EvaluativeFactorAdmin(admin.ModelAdmin):
    actions = None
    model = EvaluativeFactor
    search_fields = ("id_factor", "name")
    list_filter = ("region",)
    list_display = ('id_factor', 'name', 'quantitative_dimension')


class SupportAdmin(admin.ModelAdmin):
    model = Support
    search_fields = ('sender', 'email', 'cadastral_number')
    list_display = ('sender', 'is_close', 'email', 'cadastral_number')


class UtilizationAdmin(admin.ModelAdmin):
    actions = None
    model = Utilization
    search_fields = ("code",)
    list_display = ("code", "name")

@admin.register(Parcel)
class ParcelDisplay(admin.ModelAdmin):
    actions = None
    inlines = [EvaluativeFactorInline]
    search_fields = ("cadastral_number",)
    list_display = ('cadastral_number',)



@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    class ParserTaskInline(admin.TabularInline):
        model = ParserTask
        extra = 0

    search_fields = ("name",)
    list_display = ("region", "name", "source_url")
    inlines = [ParserTaskInline,]

class SubGroupAppraiseInline(admin.TabularInline):
    model = SubgroupAppraise
    extra = 0


class GroupAppraiseAdmin(admin.ModelAdmin):
    model = GroupAppraise
    list_display = ("group_id", "name", "region", "type")
    inlines = (SubGroupAppraiseInline,)
    list_filter = ("region", "type",)

@admin.register(ParcelStatic)
class ParcelStaticAdmin(admin.ModelAdmin):
    actions = None
    change_list_template = "admin/provernalog/parcel/list.html"
    show_full_result_count = False
    list_max_show_all = 400000000

    def get_urls(self):
        urls = super(ParcelStaticAdmin, self).get_urls()
        my_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel)),
            path('<str:region>/', self.admin_site.admin_view(self.detail_view)),
        ]
        return my_urls + urls


    def import_excel(self, request):
        initial = {}
        if request.GET:
            parcel_form = ParcelFilter(request.GET)
            if parcel_form.is_valid():
                for key, value in parcel_form.cleaned_data.items():
                    if value:
                        initial[key] = value
                initial["region"] = initial["region"].region
                wb = convert_excel_email(initial)
                response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename="Excel.xlsx"'
                wb.close()
                return response
        else:
            return Http404


    def detail_view(self, request, region):
        context_data = {}
        initial = {"region":region}
        context_data["parcel_form"] = ParcelFilter(initial)
        if request.POST:
            parcel_form = ParcelFilter(request.POST)
            if parcel_form.is_valid():
                for key, value in parcel_form.cleaned_data.items():
                    if value:
                        initial[key] = value
                initial["region"] = initial["region"].region
            context_data["parcel_form"] = ParcelFilter(request.POST)
        qs = Parcel.objects.filter(**initial)
        context_data["app_label"] = "parcel"
        context_data['parcel'] = qs.aggregate(count_parcel=Count('cadastral_number'),
                                                        common_current_cost=Sum('current_cost'),
                                                        common_cost_intermediate=Sum('cost_intermediate'),
                                                        common_approved_cost=Sum('approved_cost'),
                                                        area__sum=Sum('area'),)
        parcel_df = qs.annotate(df=F("cost_intermediate") - F('current_cost'))
        context_data["parcel_df_up"] = parcel_df.filter(df__gt=0).aggregate(count=Count('cadastral_number'),
                                                            current_cost__sum=Sum('current_cost'),
                                                            cost_intermediate__sum=Sum('cost_intermediate'),
                                                            )
        context_data["parcel_df_down"] = parcel_df.filter(df__lt=0).aggregate(count=Count('cadastral_number'),
                                                              current_cost__sum=Sum('current_cost'),
                                                              cost_intermediate__sum=Sum('cost_intermediate'),
                                                              )

        parcel_adf = qs.annotate(adf=F("approved_cost") - F('current_cost'))
        context_data["parcel_adf_up"] = parcel_adf.filter(adf__gt=0).aggregate(count=Count('cadastral_number'),
                                                                                     current_cost__sum=Sum(
                                                                                         'current_cost'),
                                                                                     approved_cost__sum=Sum(
                                                                                         'approved_cost'),
                                                                                     )
        context_data["parcel_adf_down"] = parcel_adf.filter(adf__lt=0).aggregate(count=Count('cadastral_number'),
                                                                                       current_cost__sum=Sum(
                                                                                           'current_cost'),
                                                                                       approved_cost__sum=Sum(
                                                                                           'approved_cost'),
                                                                                       )
        return render(request, "admin/provernalog/parcel/detail.html", context_data)


    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        cities = City.objects.all()
        context = []
        for i in cities:
            region = qs.filter(region=i.region)
            if region.exists():
                parcel = region.aggregate(Count("cadastral_number"), Count("current_cost"),
                                       Count("cost_intermediate"), Count("approved_cost"),
                                       Count("group_appraise"))
                context.append(dict(region=i.region, city=i.name, **parcel))
        response.context_data["parcels"] = context
        return response



admin.site.register(EvaluativeFactor, EvaluativeFactorAdmin)
admin.site.register(Formula)
admin.site.register(Support, SupportAdmin)
admin.site.register(Utilization, UtilizationAdmin)
admin.site.register(GroupAppraise, GroupAppraiseAdmin)
