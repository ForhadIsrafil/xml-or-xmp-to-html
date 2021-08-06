import lxml.html
import json
from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xmltodict
import random
import glob
import pandas as pd
import jinja2

group_df = pd.read_csv('XMP.csv')


def render_html(coloumn_values, coloumn_values2, color_arr):
    """
    Render html page using jinja
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "index.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        # coloumn_names=coloumn_names,
        coloumn_values=coloumn_values,
        coloumn_values2=coloumn_values2,
        color_arr=color_arr,
        # address=row.Address,
        # date=get_date(),
        # invoice=row.Invoice,
        # item=row.Item,
        # amount=row.Cost
    )

    # html_path = f'{row.Name}.html'
    html_path = file_name
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()


for name in glob.glob('xmp_files/*.xmp', recursive=True):
    file_name = name.split('\\')[1].split('.')[0] + '.html'
    print(file_name)
    tree = ET.parse(name)

    # tree = ET.parse("xmp_files/Alexei - bbbronzebeach2.xmp")

    root = tree.getroot()
    # print(
    #     [elem.tag for elem in root.iter() if 'li' not in elem.tag and 'Seq' not in elem.tag and 'Alt' not in elem.tag][3:])
    elements_count = len(
        [elem.tag for elem in root.iter() if 'li' not in elem.tag and 'Seq' not in elem.tag and 'Alt' not in elem.tag][
        2:])
    # print(elements_count)
    # todo: get second part data
    group_dict = {}
    for el_no in range(elements_count - 1):
        # print(len(list(root[0][0][el_no].iter())[2:]))
        if len(list(root[0][0][el_no].iter())[2:]) > 1:
            values = ''
            for i in list(root[0][0][el_no].iter())[2:]:
                # print(list(root[0][0][el_no].iter()))
                # print(i.tag, i.text, i.attrib)
                # print(root[0][0][el_no].tag.split('}')[1])
                # print(type(i.text))
                if i.text is None or i.text != '':
                    # pass
                    # print(root[0][0][el_no].tag.split('}')[1], i.text)
                    values += i.text
                    # print(values)
            try:
                group_name = group = group_df[group_df['Tag'] == root[0][0][el_no].tag.split('}')[1]]['Group'].values[0]
                group_dict.update({'<b>'+group_name+'</b> '+root[0][0][el_no].tag.split('}')[1]: values})
            except Exception as e:
                group_name = group = group_df[group_df['Tag'] == root[0][0][el_no].tag.split('}')[1]]['Group'].values[0]
                group_dict.update({'<b>'+group_name+'</b> '+root[0][0][el_no].tag.split('}')[1]: values})
        else:
            # print(root[0][0][el_no].tag.split('}')[1])
            for i in list(root[0][0][el_no].iter())[2:]:
                # print(list(root[0][0][el_no].iter()))
                # print(i.tag, i.text, i.attrib)
                # print(type(i.text))
                if i.text is None or i.text != '':
                    # pass
                    # print(root[0][0][el_no].tag.split('}')[1], i.text)
                    try:
                        group_name = group = \
                            group_df[group_df['Tag'] == root[0][0][el_no].tag.split('}')[1]]['Group'].values[0]
                        group_dict.update({'<b>'+group_name+'</b> '+root[0][0][el_no].tag.split('}')[1]: i.text})
                    except Exception as e:
                        group_name = group = \
                            group_df[group_df['Tag'] == root[0][0][el_no].tag.split('}')[1]]['Group'].values[0]
                        group_dict.update({'<b>'+group_name+'</b> '+root[0][0][el_no].tag.split('}')[1]: i.text})

    # print(group_dict)
    gdf = pd.DataFrame([group_dict])
    # gdf.to_html('demo.html', na_rep='')
    # second_part = {}
    # for elem in root.iter():
    #     if 'Look' in elem.tag:
    #         second_part.update({'Look': elem.text if elem.text == '' else ''})

    # print(second_part)

    # type_tag = root[0][0][5]
    # value = type_tag.get('rdf:Alt')

    # for i in type_tag.iter():
    #     print(i.tag.split('}')[1])
    #     print(i.text)

    # ==================
    # todo: get first part data
    table_dict = []
    for x in root[0]:
        # print('one')
        # print(x.tag, x.attrib, x.text)
        # print(x.tag)
        for key, value in x.attrib.items():
            # print(key, value)
            # print(key.split('}')[1])
            temp = {}
            # print(key.split('}')[1], value)
            try:
                group_name = group = \
                    group_df[group_df['Tag'] == key.split('}')[1]]['Group'].values[0]
                temp['<b>'+group_name+'</b> '+key.split('}')[1]] = value
                # temp['Group'] = group_name
                table_dict.append(temp)
                # table_dict.append({'Group': group_name})
            except Exception as e:
                temp[' '+key.split('}')[1]] = value
                # temp['Group'] = 'NaN'
                table_dict.append(temp)
                # table_dict.append({'Group': group_name})

    first_part_df = pd.DataFrame([table_dict])
    for k,v in gdf.to_dict().items():
        print(k,v)
    random_colors = ['#00ad8b', '#25b9a9', '#ff3200', ]
    color_length = len(first_part_df.columns.tolist())
    color_arr = []
    for c in range(color_length):
        r = lambda: random.randint(100, 200)
        color_arr.append('#%02X%02X%02X' % (r(), r(), r()))
    render_html(first_part_df.to_dict(), gdf.to_dict(), color_arr)