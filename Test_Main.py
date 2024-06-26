# tests/test_main.py

import pytest
import requests
import json

@pytest.fixture
def uploaded_file_id():
    # Simulate file upload
    files = {'file': ('test.csv', b'test,data,to,upload\n1,2,3,4')}
    response = requests.post('http://127.0.0.1:5049/upload', files=files)
    
    # Assert HTTP response status code
    assert response.status_code == 200

    # Assert JSON response content
    json_response = response.json()
    assert json_response['message'] == 'File uploaded successfully'
    assert 'file_id' in json_response

    return json_response['file_id']


def test_uploadFile():
    # Simulate file upload
    files = {'file': ('test.csv', b'test,data,to,upload\n1,2,3,4')}
    response = requests.post('http://127.0.0.1:5049/upload', files=files)
    
    # Assert HTTP response status code
    assert response.status_code == 200

    # Assert JSON response content
    json_response = response.json()
    assert json_response['message'] == 'File uploaded successfully'
    assert 'file_id' in json_response


def test_getSummary(uploaded_file_id):
    print ("--------------- upload file id:", uploaded_file_id)
  
    response = requests.get(f'http://127.0.0.1:5049/summary/{uploaded_file_id}')

    
    json_response = response.json()
    print (json_response)
    assert 'mean' in str(json_response) 


def test_transformData(uploaded_file_id):

    print ('uploaded id:', uploaded_file_id)
    
    transformations = {
        "transformations": {
            "normalize": ["data"],
            "fill_missing": {"data": 0}
        }
    }
    response = requests.post(f'http://127.0.0.1:5049/transform/{uploaded_file_id}', json=transformations)
    
    json_response = response.json()
    assert json_response['message'] == 'Transformations applied successfully'
    assert 'file_id' in json_response


def test_visualizeData(uploaded_file_id):
  
    params = {
        'chart_type': 'histogram',
        'columns': 'data'
    }
    response = requests.get(f'http://127.0.0.1:5049/visualize/{uploaded_file_id}', params=params)
    
    json_response = response.json()
    assert 'plot_url' in json_response
    assert 'file_path' in json_response
    assert json_response['message'] == 'Visualization created successfully'

    
    plot_url = json_response['plot_url']
    plot_response = requests.get(plot_url)
    assert plot_response.status_code == 200  


# Run tests with pytest
if __name__ == '__main__':
    pytest.main()
