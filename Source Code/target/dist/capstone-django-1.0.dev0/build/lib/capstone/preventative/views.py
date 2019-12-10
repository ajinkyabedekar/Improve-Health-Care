from django.shortcuts import render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
def preventative(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            dataset = pd.read_excel(settings.BASE_DIR + uploaded_file_url)
            dataset = dataset.drop([0])
            dataset = dataset.drop([1])
            dataset = dataset.drop([95])
            dataset = dataset.rename(columns={
                'Type': 'Row Labels',
                'TRUE': 'Count of Doctors',
                'Unnamed: 2': 'Centers',
                'Unnamed: 3': 'Population',
                'Unnamed: 4': 'Areas',
                'Unnamed: 5': 'Zones',
            })
            imputer = Imputer(missing_values = 'nan', strategy = 'mean', axis = 0)
            dataset = dataset.dropna(how='any')

            maximum_doc = dataset['Count of Doctors'].groupby(dataset['Zones']).sum().max()
            max_dict = dict(dataset['Count of Doctors'].groupby(dataset['Zones']).sum())
            max_zone = list(max_dict.keys())[list(max_dict.values()).index(maximum_doc)]
            plt.scatter(dataset['Count of Doctors'], dataset['Zones'])
            plt.suptitle('Count of Doctors vs Zones')
            plt.xlabel('Count of Doctors')
            plt.ylabel('Zones')
            plt.savefig(settings.BASE_DIR + '/static/' + uploaded_file_url + '_1.png', bbox_inches = 'tight')
            plt.clf()

            sheets = pd.read_excel(settings.BASE_DIR + uploaded_file_url, sheet_name=['sum'])
            dataset = pd.concat(sheets[frame] for frame in sheets.keys())
            dataset = dataset.drop([2])
            dataset = dataset.rename(columns={
                'Unnamed: 0': 'Row Labels',
                'Unnamed: 1': 'Area',
                'Unnamed: 2': 'Count of center',
                'Unnamed: 3': 'doctors',
                'Unnamed: 4': 'pop',
                'Unnamed: 5': 'Pop/center',
                'Unnamed: 6': 'Pop/Dr',
                'Unnamed: 7': 'Dr/cr',
            })
            imputer = Imputer(missing_values = 'nan', strategy = 'mean', axis = 0)
            dataset = dataset.dropna(how='any')

            plt.scatter(dataset['Count of center'], dataset['Area'])
            plt.suptitle('Count of center vs Area')
            plt.xlabel('Count of center')
            plt.ylabel('Area')
            plt.savefig(settings.BASE_DIR + '/static/' + uploaded_file_url + '_2.png', bbox_inches = 'tight')
            plt.clf()

            plt.scatter(dataset['doctors'], dataset['Area'])
            plt.suptitle('doctors vs Area')
            plt.xlabel('doctors')
            plt.ylabel('Area')
            plt.savefig(settings.BASE_DIR + '/static/' + uploaded_file_url + '_3.png', bbox_inches = 'tight')
            plt.clf()

            plt.scatter(dataset['Pop/center'], dataset['Area'])
            plt.suptitle('Pop/center vs Area')
            plt.xlabel('Pop/center')
            plt.ylabel('Area')
            plt.savefig(settings.BASE_DIR + '/static/' + uploaded_file_url + '_4.png', bbox_inches = 'tight')
            plt.clf()

            minimum_pop = dataset['Pop/Dr'].groupby(dataset['Area']).sum().min()
            min_dict = dict(dataset['Pop/Dr'].groupby(dataset['Area']).sum())
            areas_list = []
            for i in min_dict:
                if min_dict[i] > 5000:
                    areas_list.append(list(min_dict.keys())[list(min_dict.values()).index(min_dict[i])])
            min_area = list(min_dict.keys())[list(min_dict.values()).index(minimum_pop)]
            plt.scatter(dataset['Pop/Dr'], dataset['Area'])
            plt.suptitle('Pop/Dr vs Area')
            plt.xlabel('Pop/Dr')
            plt.ylabel('Area')
            plt.savefig(settings.BASE_DIR + '/static/' + uploaded_file_url + '_5.png', bbox_inches = 'tight')
            plt.clf()

            return render(request, 'preventative.html', {'uploaded_file_url': uploaded_file_url, 'maximum_doc': maximum_doc, 'max_zone': max_zone, 'minimum_pop': int(minimum_pop), 'areas_list': areas_list, 'min_area': min_area})
        return render(request, 'preventative.html')
    except:
        return render(request, 'preventative.html', {'error': 'Please Select A File'})
