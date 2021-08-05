import lxml.html
import json
from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xmltodict
import random
import glob
import pandas as pd

# data_dict = xmltodict.parse(open("xmp_files/123PRESETS SunKissed V4.xmp", encoding='utf-8').read())
# json_data = json.dumps(data_dict)
# to_dict = json.loads(json_data)

tree = ET.parse("xmp_files/Alexei - bbbronzebeach2.xmp")

# dat = minidom.parse("xmp_files/123PRESETS SunKissed V4.xmp")
# tagname= dat.getElementsByTagName('crs:Name')
# for d in tagname[0].getElementsByTagName('rdf:Alt'):
#     print(len(d))

# for x in tree.iter('{http://ns.adobe.com/camera-raw-settings/1.0/}Name'):
#     print(x.attrib)
# print(tree.find('.//{http://ns.adobe.com/camera-raw-settings/1.0/}Name').attrib)
root = tree.getroot()
print(
    [elem.tag for elem in root.iter() if 'li' not in elem.tag and 'Seq' not in elem.tag and 'Alt' not in elem.tag][3:])
elements_count = len(
    [elem.tag for elem in root.iter() if 'li' not in elem.tag and 'Seq' not in elem.tag and 'Alt' not in elem.tag][2:])
# print(elements_count)
group_dict = {}
for el_no in range(elements_count - 1):
    # print(len(list(root[0][0][el_no].iter())[2:]))
    if len(list(root[0][0][el_no].iter())[2:]) > 1:
        values = ''

        for i in list(root[0][0][el_no].iter())[2:]:
            # print(list(root[0][0][el_no].iter()))
            # print(i.tag, i.text, i.attrib)
            # print(type(i.text))
            if i.text is None or i.text != '':
                # pass
                print(root[0][0][el_no].tag.split('}')[1], i.text)
                values += i.text
                print(values)
        group_dict.update({root[0][0][el_no].tag.split('}')[1]: values})
    else:
        for i in list(root[0][0][el_no].iter())[2:]:
            # print(list(root[0][0][el_no].iter()))
            # print(i.tag, i.text, i.attrib)
            # print(type(i.text))
            if i.text is None or i.text != '':
                # pass
                print(root[0][0][el_no].tag.split('}')[1], i.text)
                group_dict.update({root[0][0][el_no].tag.split('}')[1]: i.text})

print(group_dict)
gdf = pd.DataFrame([group_dict])
gdf.to_html('demo.html', na_rep='')
second_part = {}
for elem in root.iter():
    if 'Look' in elem.tag:
        second_part.update({'Look': elem.text if elem.text == '' else ''})

# print(second_part)

# type_tag = root[0][0][5]
# value = type_tag.get('rdf:Alt')

# for i in type_tag.iter():
#     print(i.tag.split('}')[1])
#     print(i.text)

# ==================
table_dict = {}
for x in root[0]:
    # print('one')
    # print(x.tag, x.attrib, x.text)
    for key, value in x.attrib.items():
        # print(key, value)

        # print(key.split('}')[1], value)
        temp = {}
        temp[key.split('}')[1]] = value
        table_dict.update(temp)

df = pd.DataFrame([table_dict])
dfs = pd.concat([df, gdf], axis=1, )
# print(dfs.style.set_table_styles(axis=1,))
# dfs.set_index(dfs.columns.tolist())

# print(df.columns.tolist())
template = """"
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
# <style>
# th {
#     background: red;
#     color: black;
#     text-align: left;
# }
# </style>
<body>
%s
</body>
"""
classes = 'table table-responsive table-success table-bordered table-hover table-sm'
html = template % dfs.to_html(classes=classes)

file_name = 'Alexei - bbbronzebeach2.html'
with open(file_name, 'w') as f:
    f.write(html)
f.close()
# dfs.to_html('Alexei - bbbronzebeach2.html', na_rep='', notebook=True, justify='center',
#             classes=["table-bordered","table-responsive", "table-striped", "table-hover"])
# ==================


'''
1. first part is just key value pairs visible in a table

2. but second part is grouped. for example:

<crs:ToneCurvePV2012Red>
<rdf:Seq>
<rdf:li>0, 0</rdf:li>
<rdf:li>40, 12</rdf:li>
<rdf:li>84, 58</rdf:li>
<rdf:li>124, 123</rdf:li>
<rdf:li>186, 196</rdf:li>
<rdf:li>255, 255</rdf:li>
</rdf:Seq>
</crs:ToneCurvePV2012Red>

3. also this should be grouped:

crs:HueAdjustmentRed="-11"
crs:HueAdjustmentOrange="-26"
crs:HueAdjustmentYellow="-31"
crs:HueAdjustmentGreen="-33"
crs:HueAdjustmentAqua="+22"
crs:HueAdjustmentBlue="-31"
crs:HueAdjustmentPurple="0"
crs:HueAdjustmentMagenta="0"

crs:SaturationAdjustmentRed="-18"
crs:SaturationAdjustmentOrange="-42"
crs:SaturationAdjustmentYellow="-59"
crs:SaturationAdjustmentGreen="-69"
crs:SaturationAdjustmentAqua="+41"
crs:SaturationAdjustmentBlue="-50"
crs:SaturationAdjustmentPurple="-47"
crs:SaturationAdjustmentMagenta="-46"

crs:LuminanceAdjustmentRed="0"
crs:LuminanceAdjustmentOrange="0"
crs:LuminanceAdjustmentYellow="0"
crs:LuminanceAdjustmentGreen="+41"
crs:LuminanceAdjustmentAqua="0"
crs:LuminanceAdjustmentBlue="0"
crs:LuminanceAdjustmentPurple="0"
crs:LuminanceAdjustmentMagenta="0"
'''

import jinja2


def render_html(coloumn_names, coloumn_values, color_arr):
    """
    Render html page using jinja
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "index.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        coloumn_names=coloumn_names,
        coloumn_values=coloumn_values,
        color_arr=color_arr,
        # address=row.Address,
        # date=get_date(),
        # invoice=row.Invoice,
        # item=row.Item,
        # amount=row.Cost
    )

    # html_path = f'{row.Name}.html'
    html_path = f'Alexei - bbbronzebeach2.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()

random_colors = ['#00ad8b', '#25b9a9', '#ff3200',]
color_length = len(dfs.columns.tolist())
color_arr = []
for c in range(color_length):
    r = lambda: random.randint(100,200)
    color_arr.append('#%02X%02X%02X' % (r(),r(),r()))
render_html(dfs.columns.tolist(), dfs.to_dict(), color_arr)

# for k, v in dfs.to_dict().items():
#     print(v)
