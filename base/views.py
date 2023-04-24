import logging
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from myRequest.views import UserObjectMixins
from django.contrib import messages

# Create your views here.
class Contact(UserObjectMixins,View):
    def get(self, request):
        try:
            ctx = {}
            response = {}
            username = 'None'
            ContactPage = True
            if 'authenticated' in request.session:
                authenticated = request.session['authenticated']
                if 'Name' in request.session:
                    username = request.session['Name']
                else:
                    username = request.session['Email']
            else:
                authenticated = False
        except Exception as e:
            logging.exception(e)
            messages.error(request, f'{e}')
            return redirect('index')
        ctx = {
            'authenticated':authenticated,
            "response":response,
            'username':username,
            'ContactPage':ContactPage
        }
        return render(request,'contact.html',ctx)
    
class SendMessage(UserObjectMixins,View):
    def post(self, request):
        try:
            name = request.POST.get('name')
            reply_email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            email_template = 'message.html'
            recipient_email = 'devops@kobby.co.ke'
            
            if 'authenticated' in request.session:
                authenticated = request.session['authenticated']
                
                if authenticated == True:
                    state = request.session['state'] 
                    reply_email = request.session['Email']
                    if state == 'Prospect':
                        name = request.session['Email']
                    elif state == 'Vendor':
                        name = request.session['Name']
            if ('authenticated' not in request.session and name == '') or ('authenticated' not in request.session and reply_email == ''):
                return JsonResponse({'success': False, 'error': 'email and name cannot be empty'})
            send_mail = self.send_message(name,reply_email,subject,
                                            message,email_template,recipient_email)
            if send_mail == True:
                return JsonResponse({'success': True, 'message': 'Your message has been sent. Thank you!'})
            return JsonResponse({'success': False, 'error': 'Not sent'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
class Profile(UserObjectMixins,View):
    def get(self, request):
        try:
            ctx = {}
            response = {}
            username = 'None'
            state = 'Prospect'
            ContactPage = True
            details = {}
            if 'authenticated' in request.session:
                authenticated = request.session['authenticated']
                state =  request.session['state']
                if 'Name' in request.session:
                    username = request.session['Name']
                else:
                    username = request.session['Email']
            else:
                authenticated = False
            if request.session['state'] == "Vendor":
                vendors = self.one_filter("/QyVendorDetails","EMail","eq",request.session['Email'] )
                for vendor in vendors[1]:
                    details = vendor
            elif request.session['state'] == "Prospect":
                prospect = self.one_filter("/QyProspectiveSuppliers","Email","eq",request.session['Email']) 
                for prospect in prospect[1]:
                    details = prospect
        except Exception as e:
            logging.exception(e)
            messages.error(request, f'{e}')
            return redirect('index')
        ctx = {
            'authenticated':authenticated,
            "response":response,
            'username':username,
            'ContactPage':ContactPage,
            'state':state,
            "details":details
        }
        return render(request,'profile.html',ctx)