# -*- coding: utf-8 -*-
import time
import xml.etree.ElementTree as ET
from collections import namedtuple
import xlrd
import requests



class ParseXml:
    def __init__(self, files):
        self.files = files
        self.tree = ET.parse(self.files)
        self.root = self.tree.getroot()
        self.factor = []
        self.cost = []
        self.assignation = ["Ass_Flat", "Ass_Building"]

    def get_count_parcels(self):
        count = 0
        tags = ["Parcel", "Building", "Uncompleted", "Flat", "Construction", "Real_Estate"]
        for tag in tags:
            count += len(list(self.root.iter(tag)))
        return count

    def get_factors(self):
        try:
            for el in self.root.iter():
                if "Evaluative_Factor" == el.tag:
                    init_data = dict(id_factor="", name="", description="", quantitative_dimension="")
                    init_data["id"] = []
                    init_data['value'] = []
                    for elem in el.iter():
                        if "Evaluative_Factor" == elem.tag:
                            init_data["id_factor"] = elem.attrib.get("Id_Factor")
                        if "Name_Factor" == elem.tag:
                            init_data["name"] = elem.text
                        if "Name_Factor_Desc" == elem.tag:
                            init_data["description"] = elem.text
                        if "Qualitative_Id" == elem.tag:
                            init_data["id"].append(elem.text)
                        if "Qualitative_Value" == elem.tag:
                            init_data["value"].append(elem.text)
                        if "Quantitative_Dimension" == elem.tag:
                            init_data["quantitative_dimension"] = elem.text
                    if init_data["id_factor"]:
                        self.factor.append(init_data)
        except IndexError as er:
            pass
        return self.factor


    def get_parcel(self):
        for el in self.root.iter():
            tags = ["Parcel", "Building", "Uncompleted", "Flat", "Construction", "Real_Estate"]
            if el.tag in tags:
                parcel = dict()
                try:
                    parcel["group_appraise"] = int(self.files.split("/")[-2])
                except:
                    pass
                factors = []
                values = []
                for elem in el.iter():
                    if "CadastralNumber" == elem.tag:
                        parcel["cadastral_number"] = elem.text
                    if "CadastralNumber" in elem.attrib:
                        parcel["cadastral_number"] = elem.attrib["CadastralNumber"]
                    if "Area" == elem.tag:
                        parcel["area"] = elem.text
                    if "Note" == elem.tag:
                        parcel["address"] = elem.text
                    if elem.tag in self.assignation:
                        parcel["assignation"] = elem.text
                    if "Evaluative_Factor" == elem.tag:
                        factors.append(elem.attrib["ID_Factor"])
                    if "Quantitative_Value" == elem.tag:
                        values.append(elem.text)
                    if "Qualitative_Id" == elem.tag:
                        values.append(elem.text)
                    if "DateCreated" in elem.attrib:
                        for el in elem.iter():
                            if el.tag == "CadastralCost":
                                if "Value" in el.attrib:
                                    parcel["current_cost"] = el.attrib["Value"].replace(",", ".")
                            if el.tag == "Utilization":
                                if "ByDoc" in el.attrib:
                                    parcel["bydoc"] = el.attrib["ByDoc"]
                    else:
                        if elem.tag == "Ground_Payments":
                            for el in el.iter():
                                if el.tag == "CadastralCost":
                                    if self.files.split("/")[-1].split(" ")[0] == "APPROVED_COST":
                                        parcel["approved_cost"] = el.attrib["Value"].replace(",", ".")
                                    else:
                                        parcel["cost_intermediate"] = el.attrib["Value"].replace(",", ".")
                                if el.tag == "Specific_CadastralCost":
                                    if self.files.split("/")[-1].split(" ")[0] == "APPROVED_COST":
                                        parcel["approved_specififc_cost"] = el.attrib["Value"].replace(",", ".")
                                    else:
                                        parcel["specific_cost_intermediate"] = el.attrib["Value"].replace(",", ".")
                    if "Utilization" == elem.tag:
                        if "Name_doc" in elem.attrib:
                            parcel["bydoc"] = elem.attrib["Name_doc"]
                        if "ByDoc" in elem.attrib:
                            parcel["bydoc"] = elem.attrib["ByDoc"]
                        if "Name" in elem.attrib:
                            parcel["utilization"] = elem.attrib["Name"]
                    parcel["evaluative_factors"] = factors
                    parcel["values"] = values
                yield parcel


class ParseExcel:
    def __init__(self, file, name):
        self.wb = xlrd.open_workbook(file)
        self.ws = self.wb.sheet_by_index(0)
        self.parcels = []
        self.name = name


    def write_excel_parcel(self):
        x = {}
        for column_iter in range(self.ws.ncols):
            x[self.ws.cell(0, column_iter).value] = column_iter
        for i in range(1, self.ws.nrows):
            data = dict()
            for key, value in self.name.items():
                if value is not "":
                    if key == "date_relevance":
                        data[key] = value
                    else:
                        data[key] = self.ws.cell(i, value if type(value) == int else x[value]).value
            if "cadastral_number" in data and data["cadastral_number"]:
                self.parcels.append(data)
        return self.parcels


class ParseApi:
    def __init__(self):
        self.url = "https://rosreestr.ru/api/online/fir_object/{number}"
        self.parcel = {}

    def low_priority(self, cadastral_number):
        self.parcel['cadastral_number'] = cadastral_number
        cadastral_number = cadastral_number.split(":")
        cadastral_number = [str(int(part)) for part in cadastral_number]
        cadastral_number = ':'.join(cadastral_number)
        url = self.url.format(number=cadastral_number)
        try:
            r = requests.get(url)
            if r.status_code == 204:
                return self.parcel
            else:
                data = r.json()
                self.parcel['current_cost'] = data['parcelData']["cadCost"]
                return self.parcel
        except:
            time.sleep(2)
            self.low_priority(cadastral_number)


