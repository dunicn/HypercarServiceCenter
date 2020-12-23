from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("<h2>Welcome to the HyperCar Service!</h2>")


customer_dictionary = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": [],
    "estimated_time": 0,
    "customer_ticket": 0,
    "oil_tickets": [],
    "tire_tickets": [],
    "diagnostic_tickets": [],
}

#
def menu(request):
    return render(request, "tickets/index.html")

def change_oil(request):
    service = "change_oil"
    customer_dictionary["customer_ticket"] += 1
    customer_dictionary["oil_tickets"].append(customer_dictionary["customer_ticket"])
    calculating_waiting_time(service)
    customer_dictionary["change_oil"].append(2)
    context = {"ticket": customer_dictionary}
    return render(request, "tickets/change_oil.html", context)

def inflate_tires(request):
    service = "inflate_tires"
    customer_dictionary["customer_ticket"] += 1
    customer_dictionary["tire_tickets"].append(customer_dictionary["customer_ticket"])
    calculating_waiting_time(service)
    customer_dictionary["inflate_tires"].append(5)
    context = {"ticket": customer_dictionary}
    return render(request, "tickets/inflate_tires.html", context)

def diagnostic(request):
    service = "diagnostic"
    customer_dictionary["customer_ticket"] += 1
    customer_dictionary["diagnostic_tickets"].append(customer_dictionary["customer_ticket"])
    calculating_waiting_time(service)
    customer_dictionary["diagnostic"].append(30)
    context = {"ticket": customer_dictionary}
    return render(request, "tickets/diagnostic.html", context)

def calculating_waiting_time(service):
    if customer_dictionary["customer_ticket"] <= 2:
        customer_dictionary["estimated_time"] = 0
    elif customer_dictionary["customer_ticket"] == 3:
        if 0 < len(customer_dictionary["change_oil"]) < 2:
            customer_dictionary["estimated_time"] = 2
        elif len(customer_dictionary["inflate_tires"]) == 2:
            customer_dictionary["estimated_time"] = 5
        elif len(customer_dictionary["diagnostic"]) == 2:
            customer_dictionary["estimated_time"] = 30
    else:
        oil_time = 0
        tires_time = 0
        diagnostic_time = 0
        if service == "change_oil":
            for elem in customer_dictionary["change_oil"]:
                oil_time += elem
            customer_dictionary["estimated_time"] = oil_time
        elif service == "inflate_tires":
            for elem in customer_dictionary["inflate_tires"]:
                tires_time += elem
            for elem in customer_dictionary["change_oil"]:
                oil_time += elem
            customer_dictionary["estimated_time"] = tires_time + oil_time
        elif service == "diagnostic":
            for elem in customer_dictionary["inflate_tires"]:
                tires_time += elem
            for elem in customer_dictionary["change_oil"]:
                oil_time += elem
            for elem in customer_dictionary["diagnostic"]:
                diagnostic_time += elem
            customer_dictionary["estimated_time"] = oil_time + tires_time + diagnostic_time


def processing_page(request):
    context = {"ticket": customer_dictionary}
    if request.POST.get("next_button"):
        return redirect("next/")
    else:
        return render(request, "tickets/operator.html", context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {"ticket": customer_dictionary}
        return render(request, 'tickets/operator.html', context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("next_button"):
            return redirect("/next")
        elif request.POST.get("next_button") is None:
            return redirect("/menu")


def next_page(request):
    message = ""
    if len(customer_dictionary["oil_tickets"]) + len(customer_dictionary["tire_tickets"]) + len(customer_dictionary["diagnostic_tickets"]) <= 2:
        message = "Waiting for the next client"
    elif len(customer_dictionary["oil_tickets"]) != 0:
        service = "change_oil"
        customer_dictionary["change_oil"].pop()
        calculating_waiting_time(service)
        message = "Next ticket #{}".format(customer_dictionary["oil_tickets"].pop(0))
    elif len(customer_dictionary["tire_tickets"]) != 0:
        service = "inflate_tires"
        customer_dictionary["inflate_tires"].pop()
        calculating_waiting_time(service)
        message = "Next ticket #{}".format(customer_dictionary["tire_tickets"].pop(0))
    elif len(customer_dictionary["diagnostic_tickets"]) != 0:
        service = "diagnostic"
        customer_dictionary["diagnostic"].pop()
        calculating_waiting_time(service)
        message = "Next ticket #{}".format(customer_dictionary["diagnostic_tickets"].pop(0))
    else:
        message = "Waiting for the next client"
    message_dict = {"message": ""}
    message_dict["message"] = message
    context = {"message": message_dict}
    return render(request, "tickets/next.html", context)
