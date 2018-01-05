# -*- coding:GBK -*-
import xml.etree.ElementTree as ET
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from  collections import namedtuple

#####################################       Ѱ�ұ��վ�µ��ļ��б�ǩ
def tag_get(tag):
	global tag_target
	next_name=tag.getchildren()[0]
	next_folder = tag.getchildren()[1]
	print(next_name.text)
	bdz=bdz_re.match(next_name.text)
	if bdz :
		tag_target=next_folder.getchildren()[1]
		return
	else:
		tag_get(next_folder)



######################################		���������
def get_dist_max(point1,point2):     #		��������
	dist =float(np.square(point1.jd -point2.jd) + np.square(point1.wd- point2.wd))
	return dist
def get_dist_min(point1,point2):     #		����С����
	dist = np.square(point1.jd -point2.jd) + np.square(point1.wd- point2.wd)
	if dist==0:
		return 100
	else:
		return dist



######################################       ����·��������
def order_list(maxdist_p,line_f):
	list1_order=[]
	line_tmp=line_f[:]
	list1_order.append(maxdist_p[1])
	
	for i in range(len(line_tmp)):
		if len(list1_order)==len(line_tmp):
			break
		else:
			# print(list1_order)
			# print('first::line_tmp:', line_tmp)
			mindist_p=get_mindist(list1_order[i],line_tmp)
			# print(mindist_p)
			while mindist_p in list1_order:
			# if mindist_p in list1_order:
				line_tmp[mindist_p]=line_tmp[mindist_p]._replace(jd=float(10000),wd=float(0))
				# print('line_tmp:',line_tmp)
				mindist_p = get_mindist(list1_order[i], line_tmp)
				# print(mindist_p)
				# list1_order.append(mindist_p)
			# else:
			list1_order.append(mindist_p)
			line_tmp = line_f[:]
	return list1_order




######################################      ����������λ��
def get_maxdist(list_vec_f):
	list=[]
	for i in list_vec_f:
		# print(line[i.max_p],line[i.root_p])
		list.append(get_dist_max(line[i.max_p],line[i.root_p]))
	# print(list)
	np_list = np.array(list)
	max_p = np.where(np_list == np.max(np_list))[0][0]
	# print(line[max_p],line[list_vec[max_p].root_p])
	# max_dist=get_dist_max(line[max_p],line[list_vec[max_p].max_p])
	# print(max_dist)
	max_p2=list_vec[max_p].max_p
	return [max_p,max_p2]


######################################      ������С�����λ��
def get_mindist(poi,line_f):
	list_min=[]                       ##���ĳ�������������С����
	for i in range(len(line_f)):
		list_min.append(get_dist_min(line_f[poi],line_f[i]))
	np_list2=np.array(list_min)
	min_p = np.where(np_list2 == np.min(np_list2))[0][0]  #����Сֵλ��
	return min_p



######################################      ����ĳ���������λ��
def get_pointplc(poi,line_f):
	list_max=[]                       ##���ĳ�����������������
	for i in range(len(line_f)):
		list_max.append(get_dist_max(line_f[poi],line_f[i]))
	np_list1=np.array(list_max)
	max_p = np.where(np_list1==np.max(np_list1))   #�����ֵλ��
	return max_p[0][0]



######################################      ��order����ͼ
def draw(list,line_f):
	jd_list1=[]
	wd_list1=[]
	for i in list:
		# print(i)
		jd_list1.append(line_f[i].jd)
		wd_list1.append(line_f[i].wd)
	plt.figure(2)
	# print(jd_list1)
	# print(wd_list1)
	plt.plot(jd_list1,wd_list1)


######################################      ��list_order�����line,�����ַ�������
def orderlist_line(order,line_f):
	line_use=line_f[:]
	line_result=[]
	for i in order:
		line_result.append(str(line_use[i].jd)+','+str(line_use[i].wd)+','+'0')
	return  line_result

######################################                        ������
Point=namedtuple('point',['id','jd','wd']) # ����㣨���ȣ�γ�ȣ�
point_mesg=namedtuple('vec',['root_p','max_p'])   #�����ŵ㣨��Сֵ�����ֵ��
tag_target=None
tree= ET.parse('2017.xml')
root = tree.getroot()
tag1 = root.getchildren()[0]    #get document
tag2 = tag1.getchildren()[1]  #get  first_folder
bdz_re=re.compile(r".*վ\b")
jd_list = []  # ��ž���
wd_list = []  # ���γ��
line = []   #��Ÿ��㾭γ��
place=[]
tag_get(tag2)
for i in tag_target.iter("coordinates"):
	place.append(i.text)
fen = re.compile(',')

for i in place:     #��ž�γ��
	total = fen.split(i)
	line.append(Point(id=place.index(i),jd=float(total[0]),wd=float(total[1])))
	jd_list.append(float(total[0]))
	wd_list.append(float(total[1]))
	
# for i in range(len(line)):  ##��������
# 	plt.figure(1)
# 	plt.plot(line[i].jd,line[i].wd, 'bs')
	
list_vec=[]   #��Ÿ���������С����

for i in range(len(line)):
	list_vec.append(point_mesg(root_p=i,max_p=get_pointplc(i,line)))

print(list_vec)
max_dist_point=get_maxdist(list_vec)
print(max_dist_point)
print(line)
list_r_order=order_list(max_dist_point,line)
# plt.figure(3)
# plt.plot(jd_list,wd_list)    ##������������
# draw(list_r_order,line)
print(list_r_order)
right_list=orderlist_line(list_r_order,line)
print(right_list)
str_right_list=','.join(right_list)
print (str_right_list)
# plt.show()

########################################################################################################    ����xml�ڵ�

Placemark = ET.Element('Placemark')  # Element(tag, attrib={}, **extra)
name = ET.SubElement(Placemark,'name')  # SubElement(parent, tag, attrib={}, **extra)
name.text = tag_target.getchildren()[0].text
Style = ET.SubElement(Placemark,'Style')
LineStyle = ET.SubElement(Style,'LineStyle')
color = ET.SubElement(LineStyle,'color')
color.text = '7fffff80'
width = ET.SubElement(LineStyle,'width')
width.text = '4'
IconStyle = ET.SubElement(Style,'IconStyle')
Icon = ET.SubElement(IconStyle,'Icon')
MultiGeometry = ET.SubElement(Placemark,'MultiGeometry')
Point = ET.SubElement(MultiGeometry,'Point')
coordinates = ET.SubElement(Point,'coordinates')
coordinates.text=right_list[0]
LineString = ET.SubElement(MultiGeometry,'LineString')
coordinates = ET.SubElement(LineString,'coordinates')
coordinates.text = str_right_list

tag_target.append(Placemark)

# write(file, encoding="us-ascii", xml_declaration=None, default_namespace=None, method="xml")
tree.write('2017_updated.xml', encoding='utf-8',xml_declaration=True)
# print(order_list(line))





	







	


	


