#!/usr/bin/env python3
"""
Backend API Test Suite for Service Form CRUD Operations
Tests the Service Form endpoints with admin authentication
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://serviceapp-forms.preview.emergentagent.com/api"
ADMIN_USERNAME = "lenex"
ADMIN_PASSWORD = "NTAG424DNA.3423"

class ServiceFormTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.created_form_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_data": response_data
        })
    
    def login_admin(self):
        """Login with admin credentials and get JWT token"""
        print("\n=== ADMIN LOGIN TEST ===")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": ADMIN_USERNAME,
                    "password": ADMIN_PASSWORD
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                user_info = data.get("user", {})
                
                self.log_test(
                    "Admin Login",
                    True,
                    f"Successfully logged in as {user_info.get('username')} (role: {user_info.get('role')})",
                    data
                )
                return True
            else:
                self.log_test(
                    "Admin Login",
                    False,
                    f"Login failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Login request failed: {str(e)}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers with JWT token"""
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_create_form(self):
        """Test POST /api/forms - Create new service form"""
        print("\n=== CREATE FORM TEST ===")
        
        form_data = {
            "formNumber": 1,
            "customerName": "Test Müşteri A.Ş.",
            "authorizedPerson": "Ahmet Yılmaz",
            "address": "Test Mahallesi Test Sokak No:1 İstanbul",
            "phone": "+90 555 123 4567",
            "projectNo": "PRJ-2024-001",
            "email": "ahmet@test.com",
            "date": "2024-06-15T12:00:00Z",
            "startTime": "13:00",
            "endTime": "17:00",
            "serviceType": "ANLAŞMALI",
            "serviceSummary": "Test servisi",
            "description": "Test açıklama",
            "note": "Test not",
            "customerFeedback": "Memnunum",
            "materials": [
                {
                    "name": "Test Malzeme 1",
                    "quantity": "5",
                    "unit": "Adet",
                    "unitPrice": "100.50",
                    "totalPrice": 502.5
                }
            ],
            "materialTotal": 502.5,
            "serviceFee": 1000.0,
            "amount": 1502.5,
            "kdv": 300.5,
            "grandTotal": 1803.0,
            "customerSignature": "",
            "technicianSignature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/forms",
                json=form_data,
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.created_form_id = data.get("id")
                
                self.log_test(
                    "Create Form",
                    True,
                    f"Form created successfully with ID: {self.created_form_id}",
                    data
                )
                return True
            else:
                self.log_test(
                    "Create Form",
                    False,
                    f"Form creation failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Create Form", False, f"Create form request failed: {str(e)}")
            return False
    
    def test_get_forms_list(self):
        """Test GET /api/forms - Get all forms list"""
        print("\n=== GET FORMS LIST TEST ===")
        
        try:
            response = requests.get(
                f"{self.base_url}/forms",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                forms_count = len(data) if isinstance(data, list) else 0
                
                # Check if our created form is in the list
                found_our_form = False
                if self.created_form_id and isinstance(data, list):
                    found_our_form = any(form.get("id") == self.created_form_id for form in data)
                
                message = f"Retrieved {forms_count} forms"
                if found_our_form:
                    message += f", including our created form (ID: {self.created_form_id})"
                
                self.log_test(
                    "Get Forms List",
                    True,
                    message,
                    {"forms_count": forms_count, "found_created_form": found_our_form}
                )
                return True
            else:
                self.log_test(
                    "Get Forms List",
                    False,
                    f"Get forms failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Get Forms List", False, f"Get forms request failed: {str(e)}")
            return False
    
    def test_get_single_form(self):
        """Test GET /api/forms/{form_id} - Get specific form"""
        print("\n=== GET SINGLE FORM TEST ===")
        
        if not self.created_form_id:
            self.log_test("Get Single Form", False, "No form ID available (create form test must pass first)")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/forms/{self.created_form_id}",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify key fields
                customer_name = data.get("customerName")
                form_number = data.get("formNumber")
                service_fee = data.get("serviceFee")
                
                self.log_test(
                    "Get Single Form",
                    True,
                    f"Retrieved form details - Customer: {customer_name}, Form#: {form_number}, Service Fee: {service_fee}",
                    {"form_id": self.created_form_id, "customer_name": customer_name}
                )
                return True
            else:
                self.log_test(
                    "Get Single Form",
                    False,
                    f"Get single form failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Get Single Form", False, f"Get single form request failed: {str(e)}")
            return False
    
    def test_update_form(self):
        """Test PUT /api/forms/{form_id} - Update form"""
        print("\n=== UPDATE FORM TEST ===")
        
        if not self.created_form_id:
            self.log_test("Update Form", False, "No form ID available (create form test must pass first)")
            return False
        
        # First get the current form data
        try:
            get_response = requests.get(
                f"{self.base_url}/forms/{self.created_form_id}",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if get_response.status_code != 200:
                self.log_test("Update Form", False, "Could not retrieve form for update")
                return False
            
            current_form = get_response.json()
            
            # Update the customerName
            update_data = {
                "customerName": "Güncellenmiş Müşteri",
                "authorizedPerson": current_form.get("authorizedPerson", ""),
                "address": current_form.get("address", ""),
                "phone": current_form.get("phone", ""),
                "projectNo": current_form.get("projectNo", ""),
                "email": current_form.get("email", ""),
                "date": current_form.get("date", ""),
                "startTime": current_form.get("startTime", ""),
                "endTime": current_form.get("endTime", ""),
                "serviceType": current_form.get("serviceType", ""),
                "serviceSummary": current_form.get("serviceSummary", ""),
                "description": current_form.get("description", ""),
                "note": current_form.get("note", ""),
                "materials": current_form.get("materials", []),
                "materialTotal": current_form.get("materialTotal", 0),
                "serviceFee": current_form.get("serviceFee", 0),
                "amount": current_form.get("amount", 0),
                "kdv": current_form.get("kdv", 0),
                "grandTotal": current_form.get("grandTotal", 0),
                "customerSignature": current_form.get("customerSignature", ""),
                "technicianSignature": current_form.get("technicianSignature", ""),
                "customerFeedback": current_form.get("customerFeedback", "")
            }
            
            response = requests.put(
                f"{self.base_url}/forms/{self.created_form_id}",
                json=update_data,
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                # Verify the update by getting the form again
                verify_response = requests.get(
                    f"{self.base_url}/forms/{self.created_form_id}",
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if verify_response.status_code == 200:
                    updated_form = verify_response.json()
                    new_customer_name = updated_form.get("customerName")
                    
                    if new_customer_name == "Güncellenmiş Müşteri":
                        self.log_test(
                            "Update Form",
                            True,
                            f"Form updated successfully - Customer name changed to: {new_customer_name}",
                            {"old_name": current_form.get("customerName"), "new_name": new_customer_name}
                        )
                        return True
                    else:
                        self.log_test(
                            "Update Form",
                            False,
                            f"Update verification failed - Expected 'Güncellenmiş Müşteri', got '{new_customer_name}'"
                        )
                        return False
                else:
                    self.log_test("Update Form", False, "Could not verify update")
                    return False
            else:
                self.log_test(
                    "Update Form",
                    False,
                    f"Form update failed with status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Update Form", False, f"Update form request failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Service Form CRUD tests"""
        print("🚀 Starting Service Form CRUD API Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"Admin User: {ADMIN_USERNAME}")
        print("=" * 60)
        
        # Test sequence
        tests_passed = 0
        total_tests = 0
        
        # 1. Login
        if self.login_admin():
            tests_passed += 1
        total_tests += 1
        
        # 2. Create Form
        if self.test_create_form():
            tests_passed += 1
        total_tests += 1
        
        # 3. Get Forms List
        if self.test_get_forms_list():
            tests_passed += 1
        total_tests += 1
        
        # 4. Get Single Form
        if self.test_get_single_form():
            tests_passed += 1
        total_tests += 1
        
        # 5. Update Form
        if self.test_update_form():
            tests_passed += 1
        total_tests += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Tests Passed: {tests_passed}/{total_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if tests_passed == total_tests:
            print("🎉 ALL TESTS PASSED - Service Form CRUD endpoints are working correctly!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED - Check the details above")
            
            # Show failed tests
            failed_tests = [result for result in self.test_results if not result["success"]]
            if failed_tests:
                print("\n❌ FAILED TESTS:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['message']}")
            
            return False

def main():
    """Main test execution"""
    tester = ServiceFormTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()