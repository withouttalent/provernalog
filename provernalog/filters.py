from datetime import date
from provernalog.models import City
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class GroupAppraiseFilter(SimpleListFilter):

    # super(AreaLteFilter).__init__(self, request, params, model, model_admin)
    template = 'admin/provernalog/select_filter.html'
    title = "Группа оценки"
    parameter_name = "group_appraise"


    def lookups(self, request, model_admin):
        return ((),)


    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group_appraise__group_id=self.value())




class ParcelRegionFilter(SimpleListFilter):
    title = _('Регион')

    parameter_name = 'region'

    def lookups(self, request, model_admin):
        return ((city['region'], city['name']) for city in City.objects.all().values('region', 'name'))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region=self.value())
        elif self.value() == None:
            return queryset.filter(region=62)