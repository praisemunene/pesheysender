from . credentials import MpesaAccessToken, LipanaMpesaPpassword
from datetime import datetime# import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from .models import Users, UploadedCSV, getsenderid, Notification, reseller
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.forms.models import model_to_dict
import csv
import pandas as pd
import json
from . import settings
import os
from django.core.files.base import ContentFile
import requests
from django.core.mail import send_mail
import random
def index(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'index.html', context)

def error(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, '404.html', context)

def changepassword(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'changepassword.html', context)

def creategroup(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'creategroup.html', context)

def failapi(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'failapi.html', context)

def forgotpassword(request):
    return render(request, 'forgot-password.html')


def changemypassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        
        # Retrieve the user object based on the session email
        try:
            user = Users.objects.get(email=request.session['email'])
        except Users.DoesNotExist:
            return HttpResponse("User not found", status=404)
        
        # Check if the old password matches
        if check_password(old_password, user.password):
            # Hash the new password
            hashed_new_password = make_password(new_password)
            
            # Update the user's password in the database
            user.password = hashed_new_password
            user.save()
            return HttpResponse("Password change request received successfully!")
        else:
            # Return an error response if old password doesn't match
            return HttpResponse("Old password is incorrect", status=400)

    # Handle GET requests or other cases
    return HttpResponse("This endpoint only accepts POST requests.")

def managegroup(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    uploaded_csv_data = UploadedCSV.objects.filter(useremail=user.email)

    # Pass user object and uploaded_csv_data in context
    print(uploaded_csv_data)
    context = {
        'user': user,
        'csvdata': uploaded_csv_data,
    }
    return render(request, 'managegroup.html', context)

def misreport(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'misreport.html', context)

def pay(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'pay.html', context)

def register(request):
    return render(request, 'register.html')

def senderid(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'senderid.html', context)

def sendsms(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'sendsms.html', context)

def smspersonalised(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'smspersonalized.html',context)

def smsstatus(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'smsstatus.html', context)

def templates(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    
    # Pass user object in context
    context = {'user': user}
    return render(request, 'templates.html', context)

def ussd(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    context = {'user': user}
    return render(request, 'ussd.html', context)

def admindashboard(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/profile.html')

def nav(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/mydashboard.html')


def myprofile(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    username = request.session.get('username')
    user = reseller.objects.get(username=username)
    context = {'user': user}
    return render(request, 'admin/myprofile.html', context)

def adminlogin(request):
    if request.method == 'POST':
        # Extract username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against the reseller model
        try:
            user = reseller.objects.get(username=username, password=password)
            # User authenticated, redirect to a success page or perform further actions
            request.session['username'] = username
            return redirect('admin/mydashboard')
        except reseller.DoesNotExist:
            # User not found or password incorrect, display error message
            error_message = "Invalid username or password."
            return render(request, 'admin/login.html', {'error_message': error_message})

    # Render the login page if it's a GET request
    return render(request, 'admin/login.html')


def adminregister(request):
    return render(request, 'admin/signup.html')


def createusers(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    context = {}
    # Retrieve context data from session if available
    if request.session.get('saved'):
        context['saved'] = True
        # Clear the session variable to prevent it from persisting
        del request.session['saved']
    return render(request, 'admin/createusers.html', context)
    

def updateusers(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    if request.method == 'POST':
        # Assuming your form fields are named accordingly
        user_id = request.POST.get('userid')
        password = request.POST.get('user_password')
        customer_id = request.POST.get('customerid')
        sms_provider_id_trans = request.POST.get('sms_provider_id_trans')
        cust_id = request.POST.get('cust_id')
        user_status = request.POST.get('userstatus')
        country_code = request.POST.get('countrycode')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        firm_name = request.POST.get('firmname')
        expired_on = request.POST.get('expired_on')
        sms_price = request.POST.get('sms_price')
        user_mode = request.POST.get('user_type')
        buffered = request.POST.get('buffered')
        campaign_user = request.POST.get('campaignuser')
        http_api = request.POST.get('httpapi')
        xml_api = request.POST.get('xmlapi')
        smpp = request.POST.get('smpp')
        panel = request.POST.get('panel')
        mis = request.POST.get('mis')
        user_mode = request.POST.get('usermode')
        address = request.POST.get('address')
        print(campaign_user)
        # Assuming you have a User model and you need to update its instance
        user = Users.objects.get(email=user_id)  # Assuming 'email' is the unique identifier

        # Update the user object with the new data
        user.password = password
        user.userstatus = user_status
        user.number = mobile
        user.address = address
        user.firmname = firm_name
        user.expiredon = expired_on
        user.price = sms_price
        user.httpapi = http_api
        user.hideno = campaign_user
        user.panel = panel
        user.mis = mis
        user.usermode = user_mode

        # Save the updated user object
        user.save()

        # Redirect to a success page or any other desired page
        return redirect('admin/updateusers') 
    users = Users.objects.all()
    context = {'users': users}  # Include 'users' in the context dictionary
    return render(request, 'admin/updateusers.html', context)





def get_user_details(request):
    if request.method == 'GET' and 'email' in request.GET:
        email = request.GET.get('email')
        try:
            user = Users.objects.get(email=email)
            user_data = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'password': user.password,
                'userstatus': user.userstatus,
                'number': user.number,
                'email': user.email,
                'address': user.address,
                'firmname': user.firmname,
                'expiredon': user.expiredon,
                'price': user.price,
                'usertype': user.usertype,
                'hideno': user.hideno,
                'httpapi': user.httpapi,
                'panel': user.panel,
                'mis': user.mis,
                'usermode': user.usermode
            }
            return JsonResponse(user_data)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)



def get_reseller_details(request):
    if request.method == 'GET' and 'username' in request.GET:
        username = request.GET.get('username')
        try:
            user = reseller.objects.get(username=username)
            user_data = {
                'username': user.username,
                'password': user.password,
                'description': user.description,
                'customername': user.customername,
                'address': user.address,
                'license': user.license,
                'createsender': user.createsender,
                'expiry': user.expiry,
                'email': user.email,
                'accountmanager': user.accountmanager,
                'priority': user.priority,
                'isadmin': user.isadmin
            }
            return JsonResponse(user_data)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_reseller_details(request):
    if request.method == 'POST':
        # Extract data from the request
        username = request.POST.get('customer')
        description = request.POST.get('desc')
        customername = request.POST.get('cust_name')
        address = request.POST.get('cust_address')
        license = request.POST.get('license')
        expiry = request.POST.get('expiry_date')
        createdon = timezone.now()
        email = request.POST.get('email')
        accountmanager = request.POST.get('sales_acc_mngr')
        priority = request.POST.get('priority')
        isadmin = request.POST.get('sender', '0')  # Default to '0' if not provided

        # Update reseller details in the database
        try:
            reseller_obj = reseller.objects.get(username=username)
            reseller_obj.description = description
            reseller_obj.customername = customername
            reseller_obj.address = address
            reseller_obj.license = license
            reseller_obj.expiry = expiry
            reseller_obj.email = email
            reseller_obj.createdon = createdon
            reseller_obj.accountmanager = accountmanager
            reseller_obj.priority = priority
            reseller_obj.isadmin = isadmin
            reseller_obj.save()
            return redirect('admin/updateresellers')
        except reseller.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reseller not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def createresellers(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    
    if request.method == 'POST':
        # Extract form data
        customer_id = request.POST.get('customer')
        password = request.POST.get('pwd1')
        description = request.POST.get('desc')
        customer_name = request.POST.get('cust_name')
        address = request.POST.get('cust_address')
        license = request.POST.get('license')
        createsender = request.POST.get('sender')
        expiry_date = request.POST.get('expiry_date')
        email = request.POST.get('email')
        account_manager = request.POST.get('sales_acc_mngr')
        priority = request.POST.get('priority')
        checkbox_agree = request.POST.get('chk_box')

        # Print form data to terminal
        new_reseller = reseller(
            username=email,
            password=password,
            description=description,
            customername=customer_name,
            address=address,
            license=license,
            createsender=createsender,
            expiry=expiry_date,
            email=email,
            accountmanager=account_manager,
            priority=priority
        )
        new_reseller.save()
        
        # For now, redirect back to the same page
        return render(request, 'admin/createresellers.html')
    else:
        return render(request, 'admin/createresellers.html')


def updateresellers(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    resellers = reseller.objects.all()
    context = {'users': resellers} 
    return render(request, 'admin/updateresellers.html', context)

def senderids(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    senderids = getsenderid.objects.all()
    context = {'senderids': senderids}
    return render(request, 'admin/senderids.html', context)


def requesttemplates(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/requesttemplates.html')


def misreports(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/misreports.html')

def creditshistory(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/creditshistory.html')

def creditassingmentusers(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/creditassingmentusers.html')



def creditassingmentreseller(request):
    if 'username' not in request.session:
        return redirect('admin/login')
    return render(request, 'admin/creditmanagementreseller.html')


def invoice(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Users.objects.get(email=request.session['email'])
    # Pass user object in context
    row_id = request.GET.get('id')
    try:
        # Retrieve the row with the given ID
        row = getsenderid.objects.get(id=row_id)
        # Serialize the row data
        row_data = {
            'id': row.id,
            'useremail': row.useremail,
            'senderid': row.senderid,
            'smstype': row.smstype,
            'serviceprovider': row.serviceprovider,
            'requestedon': row.requestedon,
            'approvedon': row.approvedon,
            'status': row.status
        }
        # Return the row data as JSON response
        context = {'user': user, 'row': row_data}
        return render(request, 'invoice.html', context)
    except getsenderid.DoesNotExist:
        # If row with given ID does not exist, return an error response
        return redirect('senderid')
    # Print the row id in the terminal

    
def admminlogout(request):
    # Clear the user's session
    request.session.flush()
    # Redirect the user to the login page
    return redirect('admin/login')

def logout(request):
    # Clear the user's session
    request.session.flush()
    # Redirect the user to the login page
    return redirect('login')

def login(request):
    return render(request, 'login.html')
# views.py


def registration(request):
    if request.method == 'POST':
        # This is an AJAX request
        query_dict = request.POST
        # Process the form data here
        
        # For example, print the form data
        first_name = query_dict.get('firstname')
        last_name = query_dict.get('lastname')
        email = query_dict.get('email')
        password = query_dict.get('password')
        verificationcode = random.randint(100000, 999999)
        existing_user = Users.objects.filter(email=email).exists()

        if existing_user:
            # User already exists, return a JSON response with an error message
            return JsonResponse({'message': 'User with this email already exists'}, status=400)
        # Create a new user instance
        else:
            new_user = Users(firstname=first_name, lastname=last_name, email=email, password=password, vercode=verificationcode)
            # Save the user to the database
            new_user.save()
            request.session['email'] = email
            send_mail(
                'Peshey notification',
                'Welcome to peshey your verification code is: ' + str(verificationcode),
                'peshey sms',  # Replace with your email address or sender name
                [email],
                fail_silently=False,
            )
            # Return a JSON response indicating success
            return JsonResponse({'message': 'Registration successful'}, status=200)
    else:
        # Handle non-AJAX requests here
        return JsonResponse({'message': 'Invalid request'}, status=400)



def loginform(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Find user by email
        user = Users.objects.filter(email=email).first()
        

        if user:
        # Check password
            if password == user.password:
                # Passwords match, login successful
                request.session['email'] = user.email
                # Return success response
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                # Passwords don't match, login failed
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'user doesnt exist'})
            
    else:
        # Redirect to login page if not a POST request
        return redirect('login')
    
def verifyemail(request):
    if request.method == 'POST':
        # Retrieve the verification code from the POST data
        vercode = request.POST.get('vercode')
        user = Users.objects.get(email=request.session['email'])
        # Add your verification logic here
        # Return a JSON response indicating success or failure
        if vercode == user.vercode:  # Replace '123456' with your actual verification code
            user.isverified = 1
            user.save()
            return JsonResponse({'success': True, 'message': 'Verification successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Verification failed'})

    # Return an error response for other request methods
    return JsonResponse({'error': 'POST method required'}, status=405)


def uploadcsv(request):
    if request.method == 'POST':
        try:
            for uploaded_file in request.FILES.getlist('csv_upload'):
                file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
                filename = uploaded_file.name
                user_email = request.session.get('email')
                custom_filename = request.POST.get('groupname')
                print(filename)
                print(custom_filename)
                

                with uploaded_file.open() as csv_file:
                    # Initialize the line count
                    mobile_count = 0
                    # Iterate over each line in the file
                    for line in csv_file:
                        # Increment the line count for each line
                        mobile_count += 1
                print(mobile_count)
                uploaded_csv = UploadedCSV.objects.create(
                    useremail=user_email,
                    filename=filename,
                    customfilename=custom_filename,
                    createdat=timezone.now(),
                    mobilecount=mobile_count - 1
                )
            return JsonResponse({'message': 'CSV file(s) uploaded successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'No files uploaded'}, status=400)


def getuserdata(request):
    try:
        # Assuming you have a 'email' field in your session
        user_email = request.session['email']
        # Retrieve the user object based on the email
        user = Users.objects.get(email=user_email)
        # Serialize user data to JSON format
        user_data = {
            'id': user.id,
            'username': user.firstname + " " + user.lastname,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            # Add more fields as needed
        }
        # Return user data as JSON response
        return JsonResponse({'user': user_data}, status=200)
    except Users.DoesNotExist:
        # Handle case where user does not exist
        return JsonResponse({'error': 'User not found'}, status=404)
    except KeyError:
        # Handle case where 'email' key is not present in session
        return JsonResponse({'error': 'Email not found in session'}, status=400)



from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import getsenderid

def applysenderid(request):
    if request.method == 'POST':
        # Extract form data
        user_email = request.session['email']
        senderid = request.POST.get('senderid')
        smstype = request.POST.get('messagetype')
        serviceprovider = request.POST.get('provider')
        requested_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Save files using default_storage
        applicationletter_file = request.FILES.get('applicationletter')
        cr12_file = request.FILES.get('compcr12')
        cr13_file = request.FILES.get('bizcr13')
        certincorp_file = request.FILES.get('compincorp')
        bussinesscert_file = request.FILES.get('bizcert')


        # Create the 'senderid' folder if it doesn't exist
        senderid_folder = os.path.join(settings.MEDIA_ROOT, 'senderid')
        os.makedirs(senderid_folder, exist_ok=True)



        applicationletter_path = default_storage.save(os.path.join('senderid', applicationletter_file.name), ContentFile(applicationletter_file.read()))
        cr12_path = default_storage.save(os.path.join('senderid', cr12_file.name), ContentFile(cr12_file.read())) if cr12_file else ''
        cr13_path = default_storage.save(os.path.join('senderid', cr13_file.name), ContentFile(cr13_file.read())) if cr13_file else ''
        certincorp_path = default_storage.save(os.path.join('senderid', certincorp_file.name), ContentFile(certincorp_file.read())) if certincorp_file else ''
        bussinesscert_path = default_storage.save(os.path.join('senderid', bussinesscert_file.name), ContentFile(bussinesscert_file.read())) if bussinesscert_file else ''

        # Save form data in the database
        getsenderid.objects.create(
            senderid=senderid,
            useremail=user_email,
            smstype=smstype,
            serviceprovider=serviceprovider,
            applicationletter=applicationletter_path,
            cr12=cr12_path,
            cr13=cr13_path,
            certincorp=certincorp_path,
            bussinesscert=bussinesscert_path,
            requestedon=requested_on
        )

        # If you want to return an HTTP response
        return HttpResponse(json.dumps({'message': 'Form data received and saved successfully.'}), content_type='application/json')
    
    # Handle other HTTP methods or cases
    return HttpResponse(json.dumps({'error': 'This endpoint only accepts POST requests.'}), content_type='application/json')




def getsenderids(request):
    if 'email' in request.session:
        user_email = request.session['email']
        sender_ids = getsenderid.objects.filter(useremail=user_email).values()
        return JsonResponse({'senderids': list(sender_ids)})
    else:
        return JsonResponse({'error': 'User email not found in session.'})


def updateprofile(request):
    if request.method == 'POST':
        # Retrieve form data
        user_email = request.session['email']
        firstname = request.POST.get('updatefirstname')
        lastname = request.POST.get('updatelastname')
        email = request.POST.get('updateemail')
        phonenumber = request.POST.get('updatephone')
        if Users.objects.filter(email=email).exclude(email=user_email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        # Get the current user's profile
        user_profile = Users.objects.get(email=user_email)

        # Update profile fields
        user_profile.firstname = firstname
        user_profile.lastname = lastname
        user_profile.email = email
        # user_profile.phonenumber = phonenumber

        # Save the updated profile
        user_profile.save()
        usersenderids = getsenderid.objects.filter(useremail=user_email)
        for usersenderid in usersenderids:
            usersenderid.useremail = email
            usersenderid.save()
        request.session['email'] = email
        notification_message = f"Your profile has been updated"
        time = timezone.now()
        notification = Notification(email=email, notification=notification_message, time=time, picture='<div class="icon-circle bg-warning"><i class="fas fa-exclamation-triangle text-white"></i></div>')
        notification.save()
        # Return a success response
        return JsonResponse({'message': 'Profile updated successfully'})

    else:
        # Handle GET request
        return JsonResponse({'error': 'GET method not allowed for this endpoint'}, status=405)


def getnotifications(request):
    if request.method == 'GET':
        user_email = request.session['email']
        # Query all notifications from the database
        notifications = Notification.objects.filter(email=user_email).values()
        # Convert QuerySet to list of dictionaries
        notifications_list = list(notifications)
        # Return notifications as JSON response
        return JsonResponse({'notifications': notifications_list})
    else:
        # Return error response for other request methods
        return JsonResponse({'error': 'GET method required'}, status=405)




def postnewuser(request):
    if request.method == 'POST':
        # Retrieve form data
        email = request.POST.get('useremail', '')
        password = request.POST.get('pwd', '')
        confirm_password = request.POST.get('pwd2', '')
        customer_id = request.POST.get('customerid', '')
        sms_provider_id_trans = request.POST.get('sms_provider_id_trans', '')
        userstatus = request.POST.get('userstatus', '')
        number = request.POST.get('countrycode', '') + request.POST.get('mobile', '')
        address = request.POST.get('address', '')
        firmname = request.POST.get('firmname', '')
        expiredon = request.POST.get('expired_on', '')
        price = request.POST.get('sms_price', '')
        usertype = request.POST.get('user_type', '')
        hideno = request.POST.get('campaignuser', '')
        httpapi = request.POST.get('httpapi', '')
        panel = request.POST.get('panel', '')
        mis = request.POST.get('mis', '')
        pollid = request.POST.get('pollid', '')
        constituency = request.POST.get('constituency', '')
        county = request.POST.get('county', '')
        wardid = request.POST.get('wardid', '')
        use_type = request.POST.get('use_type', '')
        usermode = request.POST.get('usermode', '')
        terms_agreed = request.POST.get('chk_box', '') == 'agree'
        firstname = "Peshey"
        lastname = "user"
        if usermode == 1:
            usersmode = "prepaid"
        else:
            usersmode = "postpaid"

        user = Users(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            userstatus=userstatus,
            number=number,
            address=address,
            firmname=firmname,
            expiredon=expiredon,
            price=price,
            usertype=usertype,
            hideno=hideno,
            httpapi=httpapi,
            panel=panel,
            mis=mis,
            usermode=usersmode,
            showcontacts=use_type,
            countycontact=county,
            constituencycontact=constituency,
            wardcontact=wardid,
            pollingcontact=pollid,
        )
        user.save()
        request.session['saved'] = True
        # Return a response
        return redirect("admin/createusers")
    else:
        # Handle GET request or other methods
        return redirect(login)
    



def getcontacts(request):
    # Assuming Users model is correctly defined in your app
    try:
        user = Users.objects.get(email=request.session['email'])
        countycontact = user.countycontact
        constituencycontact = user.constituencycontact
        wardcontact = user.wardcontact
        pollingcontact = user.pollingcontact
        
        # Create a context dictionary containing the contact information
        context = {
            'countycontact': countycontact,
            'constituencycontact': constituencycontact,
            'wardcontact': wardcontact,
            'pollingcontact': pollingcontact,
        }
    except Users.DoesNotExist:
        # Handle the case where the user does not exist
        context = {}
    
    # Pass the context dictionary to the template for rendering
    return render(request, 'getcontacts.html', context)


def managemycontacts(request):
    if request.method == 'GET':
        if 'email' not in request.session:
            return redirect('login')
        area_param = request.GET.get('area')
        # Check if 'area' parameter is provided
        if area_param == "null":
            return JsonResponse({'error': 'No area parameter provided'}, status=400)
        else:

            user = Users.objects.get(email=request.session['email'])
            countycontact = user.countycontact
            constituencycontact = user.constituencycontact
            wardcontact = user.wardcontact
            pollingcontact = user.pollingcontact
            if area_param == user.countycontact or area_param == user.constituencycontact \
                            or area_param == user.wardcontact or area_param == user.pollingcontact:
                api_key = 'TEST123'
                callback = 'getcontacts'
                id = area_param
                url = 'https://cmd.smsairworks.com/api/v1/'
                headers = {
                    'Api-Key': api_key,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # Assuming 'PHPSESSID' is retrieved elsewhere (e.g., login)
                    'Cookie': 'PHPSESSID=your_phpsessid'  # Replace with your actual PHPSESSID value
                }
                data = {
                    'callback': callback,
                    'contact_id': id,
                    'county_id': id,
                    'limit': 1000
                    }
                try:
                    response = requests.get(url, headers=headers, data=data)
                    response.raise_for_status()  # Raise exception for non-2xx status codes

                    # Handle successful response here
                    json_data = response.json()
                        
                        # Ensure each contact has the specified format
                    formatted_contacts = []
                    for contact in json_data['contacts']:
                        if contact['phone'] != "":
                            # Mask the phone number
                            first_six_digits = contact['phone'][:6]
                    
                            # Extract the last two digits
                            last_two_digits = contact['phone'][-2:]

                            # Mask the digits in between
                            masked_digits = '*' * (len(contact['phone']) - 6 - 2)  # Subtract 2 for the last two digits
                            
                            # Concatenate the first 6 digits, masked digits, and last two digits
                            masked_phone = first_six_digits + masked_digits + last_two_digits
                            
                            # Create the formatted contact
                            formatted_contact = {
                                "contact_id": contact["contact_id"],
                                "fname": contact["fname"],
                                "lname": contact["lname"],
                                "dob": contact["dob"],
                                "gender": contact["gender"],
                                "phone": masked_phone  # Replace the original phone with the masked one
                            }
                            formatted_contacts.append(formatted_contact)
                    user_dict = model_to_dict(user)
                    print(user.firmname)
                    return JsonResponse({'contacts': formatted_contacts,'user': user_dict}, json_dumps_params={'indent': 4})
                except requests.exceptions.RequestException as e:
                    print("An error occurred:", e)
                    return JsonResponse({'error': 'An error occured'}, status=500)

        # Check if the request was successful
    else:
          return JsonResponse({'error': 'you have no contacts'}, status=200)


def manageconstcontacts(request):
    if request.method == 'GET':
        if 'email' not in request.session:
            return redirect('login')
        const_param = request.GET.get('constp')
        print(const_param)  
        # Check if 'area' parameter is provided
        if const_param == "null":
            return JsonResponse({'error': 'No area parameter provided'}, status=400)
        else:

            user = Users.objects.get(email=request.session['email'])
            countycontact = user.countycontact
            constituencycontact = user.constituencycontact
            wardcontact = user.wardcontact
            pollingcontact = user.pollingcontact
            if const_param == user.constituencycontact or const_param == user.constituencycontact \
                            or const_param == user.wardcontact or const_param == user.pollingcontact:
                api_key = 'TEST123'
                callback = 'getcontacts'
                id = const_param
                url = 'https://cmd.smsairworks.com/api/v1/'
                headers = {
                    'Api-Key': api_key,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # Assuming 'PHPSESSID' is retrieved elsewhere (e.g., login)
                    'Cookie': 'PHPSESSID=your_phpsessid'  # Replace with your actual PHPSESSID value
                }
                data = {
                    'callback': callback,
                    'constituency_id': id,
                    'constituency_id': id,
                    'limit': 1000
                    }
                try:
                    response = requests.get(url, headers=headers, data=data)
                    response.raise_for_status()  # Raise exception for non-2xx status codes

                    # Handle successful response here
                    json_data = response.json()
                        
                        # Ensure each contact has the specified format
                    formatted_contacts = []
                    for contact in json_data['contacts']:
                        if contact['phone'] != "":
                            # Mask the phone number
                            first_six_digits = contact['phone'][:6]
                    
                            # Extract the last two digits
                            last_two_digits = contact['phone'][-2:]

                            # Mask the digits in between
                            masked_digits = '*' * (len(contact['phone']) - 6 - 2)  # Subtract 2 for the last two digits
                            
                            # Concatenate the first 6 digits, masked digits, and last two digits
                            masked_phone = first_six_digits + masked_digits + last_two_digits
                            
                            # Create the formatted contact
                            formatted_contact = {
                                "contact_id": contact["contact_id"],
                                "fname": contact["fname"],
                                "lname": contact["lname"],
                                "dob": contact["dob"],
                                "gender": contact["gender"],
                                "phone": masked_phone  # Replace the original phone with the masked one
                            }
                            formatted_contacts.append(formatted_contact)
                
                    return JsonResponse({'contacts': formatted_contacts}, json_dumps_params={'indent': 4})
                except requests.exceptions.RequestException as e:

                    print("An error occurred:", e)
                    return JsonResponse({'error': 'An error occured'}, status=500)

            # Check if the request was successful
            else:
                return JsonResponse({'error': 'you have no contacts'}, status=200)
            

def managewardcontacts(request):
    if request.method == 'GET':
        if 'email' not in request.session:
            return redirect('login')
        ward_param = request.GET.get('ward')
        print(ward_param)  
        # Check if 'area' parameter is provided
        if ward_param == "null":
            return JsonResponse({'error': 'No area parameter provided'}, status=400)
        else:

            user = Users.objects.get(email=request.session['email'])
            countycontact = user.countycontact
            constituencycontact = user.constituencycontact
            wardcontact = user.wardcontact
            pollingcontact = user.pollingcontact
            if ward_param == user.wardcontact:
                api_key = 'TEST123'
                callback = 'getcontacts'
                id = ward_param
                url = 'https://cmd.smsairworks.com/api/v1/'
                headers = {
                    'Api-Key': api_key,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # Assuming 'PHPSESSID' is retrieved elsewhere (e.g., login)
                    'Cookie': 'PHPSESSID=your_phpsessid'  # Replace with your actual PHPSESSID value
                }
                data = {
                    'callback': callback,
                    'ward_id': id,
                    'limit': 1000
                    }
                try:
                    response = requests.get(url, headers=headers, data=data)
                    response.raise_for_status()  # Raise exception for non-2xx status codes

                    # Handle successful response here
                    json_data = response.json()
                        
                        # Ensure each contact has the specified format
                    formatted_contacts = []
                    for contact in json_data['contacts']:
                        if contact['phone'] != "":
                            # Mask the phone number
                            first_six_digits = contact['phone'][:6]
                    
                            # Extract the last two digits
                            last_two_digits = contact['phone'][-2:]

                            # Mask the digits in between
                            masked_digits = '*' * (len(contact['phone']) - 6 - 2)  # Subtract 2 for the last two digits
                            
                            # Concatenate the first 6 digits, masked digits, and last two digits
                            masked_phone = first_six_digits + masked_digits + last_two_digits
                            
                            # Create the formatted contact
                            formatted_contact = {
                                "contact_id": contact["contact_id"],
                                "fname": contact["fname"],
                                "lname": contact["lname"],
                                "dob": contact["dob"],
                                "gender": contact["gender"],
                                "phone": masked_phone  # Replace the original phone with the masked one
                            }
                            formatted_contacts.append(formatted_contact)
                
                    return JsonResponse({'contacts': formatted_contacts}, json_dumps_params={'indent': 4})
                except requests.exceptions.RequestException as e:

                    print("An error occurred:", e)
                    return JsonResponse({'error': 'An error occured'}, status=500)

            # Check if the request was successful
            else:
                return JsonResponse({'error': 'you have no contacts'}, status=200)

def managepollingcontacts(request):
    if request.method == 'GET':
        if 'email' not in request.session:
            return redirect('login')
        polling_param = request.GET.get('polling')
        print(polling_param)  
        # Check if 'area' parameter is provided
        if polling_param == "null":
            return JsonResponse({'error': 'No area parameter provided'}, status=400)
        else:

            user = Users.objects.get(email=request.session['email'])
            countycontact = user.countycontact
            constituencycontact = user.constituencycontact
            wardcontact = user.wardcontact
            pollingcontact = user.pollingcontact
            if polling_param == user.pollingcontact:
                api_key = 'TEST123'
                callback = 'getcontacts'
                id = polling_param
                url = 'https://cmd.smsairworks.com/api/v1/'
                headers = {
                    'Api-Key': api_key,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # Assuming 'PHPSESSID' is retrieved elsewhere (e.g., login)
                    'Cookie': 'PHPSESSID=your_phpsessid'  # Replace with your actual PHPSESSID value
                }
                data = {
                    'callback': callback,
                    'polling_station_id': id,
                    'limit': 1000
                    }
                try:
                    response = requests.get(url, headers=headers, data=data)
                    response.raise_for_status()  # Raise exception for non-2xx status codes

                    # Handle successful response here
                    json_data = response.json()
                        
                        # Ensure each contact has the specified format
                    formatted_contacts = []
                    for contact in json_data['contacts']:
                        if contact['phone'] != "":
                            # Mask the phone number
                            first_six_digits = contact['phone'][:6]
                    
                            # Extract the last two digits
                            last_two_digits = contact['phone'][-2:]

                            # Mask the digits in between
                            masked_digits = '*' * (len(contact['phone']) - 6 - 2)  # Subtract 2 for the last two digits
                            
                            # Concatenate the first 6 digits, masked digits, and last two digits
                            masked_phone = first_six_digits + masked_digits + last_two_digits
                            
                            # Create the formatted contact
                            formatted_contact = {
                                "contact_id": contact["contact_id"],
                                "fname": contact["fname"],
                                "lname": contact["lname"],
                                "dob": contact["dob"],
                                "gender": contact["gender"],
                                "phone": masked_phone  # Replace the original phone with the masked one
                            }
                            formatted_contacts.append(formatted_contact)
                
                    return JsonResponse({'contacts': formatted_contacts}, json_dumps_params={'indent': 4})
                except requests.exceptions.RequestException as e:

                    print("An error occurred:", e)
                    return JsonResponse({'error': 'An error occured'}, status=500)

            # Check if the request was successful
            else:
                return JsonResponse({'error': 'you have no contacts'}, status=200)
    
def managecontacts(request):
    user = Users.objects.get(email=request.session['email'])
    context = {'user': user}
    return render(request, 'managecontacts.html',context)

def getconstcontacts(request):
    return render(request, 'getconstcontacts.html')


def sendnotification(request):
    if request.method == 'POST':
        # Retrieve all users
        users = Users.objects.all()
        
        # Extract emails from users
        emails = [user.email for user in users]
        
        # Get the message from the POST request
        message = request.POST['message']
        
        # Send SMS to each email
        for email in emails:
            send_mail(
                'Peshey notification',
                message,
                'peshey sms',  # Replace with your email address or sender name
                [email],
                fail_silently=False,
            )
            time = timezone.now()
            notification = Notification(email=email, notification=message, time=time, picture='<div class="icon-circle bg-warning"><i class="fas fa-exclamation-triangle text-white"></i></div>')
            notification.save()
            
       
        return render(request, 'admin/sendnotification.html')
        
    else:
        return render(request, 'admin/sendnotification.html')
    
def getwardcontacts(request):
    return render(request, 'getwardcontacts.html')

def getpollingcontacts(request):
    return render(request, 'getpollingcontacts.html')

def submitsms(request):
    return render(request, 'submitsms.html')

def emailverification(request):
    return render(request, 'emailverification.html')

def paympesa(request):
    if request.method == "POST":
        phone = request.POST['mpesanumber']
        amount = request.POST['mpesaamount']
        user_email = request.session.get('useremail')
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://www.pepspayz.com/dashboard/callback",
            "AccountReference": "Peshey sms",
            "TransactionDesc": "sms bulk purchase"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse({'success': phone})