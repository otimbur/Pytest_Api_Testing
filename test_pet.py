from flask import json
from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/0"

    get_pet_response = api_helpers.get_api_data(test_endpoint)

    assert get_pet_response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    #The error on this was on the schema - name has to by of type String NOT integer 
    validate(instance=get_pet_response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''

#As a note, for debugging purposes and a easy way to see the response the following method can be used
# json.dumps will structure the jason in a easy readable format but as a string so we are not using it in our test 
# get_pet_data = json.dumps(get_pet_by_status_response.json(), indent=4)
 
@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }
  
    get_pet_by_status_response = api_helpers.get_api_data(test_endpoint, params)

    assert get_pet_by_status_response.status_code == 200

    get_pet_data = get_pet_by_status_response.json()
    print(get_pet_data)

    #Validate that content-type: application/json 
    assert get_pet_by_status_response.headers["content-type"] == "application/json"

    for pet in get_pet_data:
        assert pet["status"] == status
        #Validate the schema
        validate(instance=pet, schema=schemas.pet)
    

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("pet_id", ["4", "1000", "5"])
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"
    
    error_get_pet_response = api_helpers.get_api_data(test_endpoint)

    assert error_get_pet_response.status_code == 404
    response_body = error_get_pet_response.json()
   
    assert f'Pet with ID {pet_id} not found.' in response_body["message"]
    # Question: {'message': 'Pet with ID 5 not found. You have requested this URI [/pets/5] but did you mean /pets/<int:pet_id> ?'}
    #How i get a source of truth to asser the Message 
        
pass