


text_cost_intermediate = r'''
<?xml version="1.0" encoding="UTF-8"?>
<Parcel CadastralNumber="18:01:023007:232">
    <Ground_Payments>
        <Specific_CadastralCost Value="24577.7100" Unit="1002" /><CadastralCost Value="798775.5700" Unit="383" />
</Ground_Payments>
</Parcel>
'''

text_fd_parcel_state = r'''<?xml version="1.0" encoding="UTF-8"?>
<Real_Estate ID_Group="2">
    <CadastralNumber>51:02:0060301:34</CadastralNumber>
    <Type>002001001000</Type>
    <Specific_CadastralCost Value="104.09" Unit="1002"/>
    <Area>20061</Area>
    <Location>
        <Region>51</Region>
    </Location>
    <Date_valuation>2018-01-01</Date_valuation>
</Real_Estate>

'''

text_fd_factor_state = r'''<?xml version="1.0" encoding="UTF-8"?>
<Evaluative_Factor Id_Factor="3" Type="2">
<Name_Factor>Местоположение</Name_Factor>
<Name_Factor_Desc>Фактор отражающий изменение цены 1 кв.м. при изменении площади объекта недвижимости</Name_Factor_Desc>
<QualitativeValues>
    <QualitativeValue>
        <Qualitative_Id>3_1</Qualitative_Id>
        <Qualitative_Value>I</Qualitative_Value>
    </QualitativeValue>
    <QualitativeValue>
        <Qualitative_Id>3_2</Qualitative_Id>
        <Qualitative_Value> II</Qualitative_Value>
    </QualitativeValue>
    <QualitativeValue>
        <Qualitative_Id>3_3</Qualitative_Id>
        <Qualitative_Value> III</Qualitative_Value>
    </QualitativeValue>
    <QualitativeValue>
        <Qualitative_Id>3_4</Qualitative_Id>
        <Qualitative_Value> IV</Qualitative_Value>
    </QualitativeValue>
        <QualitativeValue><Qualitative_Id>3_5</Qualitative_Id>
        <Qualitative_Value> V</Qualitative_Value>
    </QualitativeValue>
</QualitativeValues>
</Evaluative_Factor>
'''