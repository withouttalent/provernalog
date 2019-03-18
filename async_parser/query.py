from provernalog.models import *
from django.conf import settings
from decimal import Decimal, InvalidOperation
import sys


class WriteQuery:
    def __init__(self, region, task_file, group_type=None, date_relevance=None):
        self.task_file = task_file
        self.region = region
        self.type = group_type
        self.date_relevance = date_relevance

    def write_parcel(self, parcel, factors=None):
        if settings.DEBUG:
            print(parcel)
        try:
            evaluative_factors = parcel.pop("evaluative_factors") if parcel.get(
                "evaluative_factors") is not None else None
            values = parcel.pop("values") if parcel.get("values") is not None else None
            parcel_query = self.write_query_parcel(parcel)
            if evaluative_factors and factors:
                self.aggregator_factors(factors, evaluative_factors, values, parcel_query)
            self.task_file.parsed_parcels += 1
            self.task_file.save()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.task_file.errors += f"{parcel['cadastral_number']}: {str(exc_value)}\n"
            self.task_file.save()

    def aggregator_factors(self, factors, evaluative_factors, values, parcel_query):
        for factor in factors:
            if factor["id_factor"] in evaluative_factors:
                for index, evaluative_factor in enumerate(evaluative_factors):
                    if evaluative_factor == factor["id_factor"]:
                        evl_fac = EvaluativeFactor.objects.get_or_create(
                            id_factor=factor["id_factor"],
                            name=factor["name"],
                            region=self.region,
                            description=factor["description"],
                            quantitative_dimension=factor["quantitative_dimension"])[0]
                        if factor['id'] and values[index] in factor['id']:
                            id_index = factor["id"].index(values[index])
                            value = factor["value"][id_index]
                        else:
                            value = values[index]
                            try:
                                value = Decimal(value).__format__('.2f')
                            except InvalidOperation:
                                pass
                        try:
                            value_factor, _ = ValueFactor.objects.get_or_create(parcel=parcel_query,
                                                                                evaluative_factor=evl_fac)
                            value_factor.qualitative_value = value
                            value_factor.save()
                        except ValueFactor.MultipleObjectsReturned:
                            ValueFactor.objects.filter(parcel=parcel_query).delete()

    def write_query_parcel(self, parcel):
        if parcel.get("utilization"):
            utilization = Utilization.objects.filter(code=str(parcel.pop('utilization')))
            if utilization.exists():
                parcel["utilization"] = utilization[0]
        if parcel.get("group_appraise"):
            group_appraise = GroupAppraise.objects.filter(group_id=parcel.pop("group_appraise"),
                                                          type=self.type, region=self.region)
            if group_appraise.exists():
                parcel["group_appraise"] = group_appraise[0]
        parcel_query = Parcel.objects.update_or_create(
            cadastral_number=parcel["cadastral_number"],
            region=self.region, defaults=parcel)[0]
        return parcel_query
