"""
VIEWS - project information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the PROJECT INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""

from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *


@login_required(login_url='login')
def information_project_costs(request, project_id):
    if request.method == "POST":
        form = information_project_costs_form(request.POST, request.FILES)
        if form.is_valid():
            cost_description = form.cleaned_data['cost_description']
            cost_amount = form.cleaned_data['cost_amount']
            if ((not cost_description == '') and ((cost_amount <= 0) or (cost_amount >= 0))):
                submit_cost = costs(
                    project_id=project.objects.get(pk=project_id),
                    cost_description=cost_description,
                    cost_amount=cost_amount,
                    change_user=request.user,
                )
                submit_cost.save()

    #Get data
    costs_results = costs.objects.filter(project_id=project_id, is_deleted='FALSE')

    #Load template
    t = loader.get_template('NearBeach/project_information/project_costs.html')

    # context
    c = {
        'information_project_costs_form': information_project_costs_form(),
        'costs_results': costs_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_project_customers(request, project_id):
    if request.method == "POST":
        # The user has tried adding a customer
        customer_id = int(request.POST.get("add_customer_select"))

        submit_customer = project_customers(
            project_id=project.objects.get(pk=project_id),
            customer_id=customers.objects.get(pk=customer_id),
            change_user=request.user,
        )
        submit_customer.save()

    #Get data
    project_results = project.objects.get(project_id=project_id)

    #Cursor for custom SQL :)
    cursor = connection.cursor()

    cursor.execute("""
    		SELECT DISTINCT 
    		  customers.customer_id
    		, customers.customer_first_name || ' ' || customers.customer_last_name AS customer_name

    		FROM
    		  project 
    		, organisations LEFT JOIN customers
    			ON organisations.organisations_id = customers.organisations_id_id

    		WHERE 1=1
    		AND project.organisations_id_id = organisations.organisations_id

    		AND customers.customer_id NOT IN (SELECT DISTINCT project_customers.customer_id_id
    					FROM project_customers
    					WHERE 1=1
    					AND project_customers.project_id_id = project.project_id
    					AND project_customers.is_deleted = 'FALSE')


    		-- LINKS --
    		AND organisations.organisations_id = %s
    		AND project.project_id = %s
    		-- END LINKS --
    	""", [project_results.organisations_id_id, project_id])
    new_customers_results = namedtuplefetchall(cursor)

    cursor.execute("""
    		SELECT DISTINCT
    		  customers.customer_first_name
    		, customers.customer_last_name
    		, project_customers.customer_description
    		, customers.customer_email
    		, customers_campus_information.campus_nickname
    		, customers_campus_information.customer_phone
    		FROM
    		  customers LEFT JOIN 
    			(SELECT * FROM customers_campus join organisations_campus ON customers_campus.campus_id_id = organisations_campus.id) as customers_campus_information
    			ON customers.customer_id = customers_campus_information.customer_id_id
    		, project_customers
    		WHERE 1=1
    		AND customers.customer_id = project_customers.customer_id_id
    		AND project_customers.project_id_id = %s
    	""", [project_id])
    project_customers_results = namedtuplefetchall(cursor)

    t = loader.get_template('NearBeach/project_information/project_customers.html')

    # context
    c = {
        'project_results': project_results,
        'new_customers_results': new_customers_results,
        'project_customers_results': project_customers_results,
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def information_project_history(request, project_id):
    if request.method == "POST":
        form = information_project_history_form(request.POST, request.FILES)
        if form.is_valid():
            project_history_results = form.cleaned_data['project_history']

            if not project_history_results == '':
                current_user = request.user

                project_id_instance = project.objects.get(pk=project_id)

                data = project_history(
                    project_id=project_id_instance,
                    user_id=current_user,
                    project_history=project_history_results,
                    user_infomation=current_user.id,
                    change_user = request.user,
                )
                data.save()
        else:
            print(form.errors)

    project_history_results = project_history.objects.filter(
        project_id=project_id,
        is_deleted="FALSE",
    )

    t = loader.get_template('NearBeach/project_information/project_history.html')

    # context
    c = {
        'information_project_history_form': information_project_history_form(),
        'project_history_results': project_history_results,
        'project_id': project_id,
    }

    return HttpResponse(t.render(c, request))



# Extra functionality
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from collections import namedtuple
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]