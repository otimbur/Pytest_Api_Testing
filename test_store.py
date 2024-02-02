from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

#Firt we will post an Order
@pytest.fixture
def order_id():
    # This function now acts as a fixture
    test_endpoint = "/store/order"
    payload = {
        "pet_id": 0
        }
    get_order_response = api_helpers.post_api_data(test_endpoint, payload)
    assert get_order_response.status_code == 201
    order_data = get_order_response.json()

    validate(instance=order_data, schema=schemas.order)
    return order_data["id"]

@pytest.mark.parametrize("status", ["available"])
def test_patch_order_by_id(order_id, status):
    # This test uses the order_id from the fixture to patch the order
    test_endpoint = f"/store/order/{order_id}"

    payload = {"status": status}
    get_order_patch_response = api_helpers.patch_api_data(test_endpoint, payload)

    assert get_order_patch_response.status_code == 200
    order_patch_data = get_order_patch_response.json()

    assert order_patch_data["message"] == 'Order and pet status updated successfully'

# Validate that the pach is true

def status_update():
    test_endpoint = "/pets/0"

    get_pet_response = api_helpers.get_api_data(test_endpoint)
    
    assert get_pet_response.status_code == 200

    response_data = get_pet_response.json()

    assert response_data['status'] == 'pending'