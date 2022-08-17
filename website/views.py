from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import ACdatum, FanData  # FanData
from . import db
from .Backend_Scripts import AC_Calc
from .Backend_Scripts.AC_Calc import input_request as inp
from .Backend_Scripts.Alt import fan_price
from .Backend_Scripts.Tracker import plot_graph, scatter, pie_chart

views = Blueprint('views', __name__)

@views.route('')
def default():
    return render_template("home.html", user=current_user)


@views.route('home')
def home():
    return redirect(url_for("views.default"))
    # redirects to default page for people who search url/home


@views.route('base')
@login_required
def webflow():
    return render_template("base2.html", user=current_user)


@views.route('aircalculator', methods=['GET', 'POST'])
@login_required
def aircalculator():
    global recent_bill_iter
    if request.method == 'POST':
        #error checking:

        KwH, GOT = AC_Calc.KwH(current_user.BTU_rating, 
                                current_user.wattage, 
                                current_user.typ.lower() if current_user.typ != None else None, 
                                current_user.size.lower() if current_user.size != None else None)
        res_iter = AC_Calc.Price(KwH, current_user.EER, inp('hours'), inp('temp'), current_user.state,
                                 inp('major-city'), inp('month'), inp('day-avg-temp'), inp('day-high-temp'),
                                 inp('save'))
        sugg_iter = AC_Calc.sugg_temp(res_iter[0], res_iter[1], res_iter[3] - res_iter[2], res_iter[3],
                                      current_user.budget, current_user.priority)
        if request.form.get("save") == "1":
            if len(current_user.ACdata) > 0:
                if res_iter[0] < current_user.ACdata[0].estimated_bill: #if current estimated bill less than first estimated bill
                    current_user.totalMoneySaved += current_user.ACdata[0].estimated_bill-round(res_iter[0],2)
            new_ACdatum = ACdatum(hours=res_iter[1],
                                  temp=res_iter[2],
                                  sugg_hours = sugg_iter[0],
                                  sugg_temp = int(request.form.get("temp"))+round(sugg_iter[1],2),
                                  estimated_bill=round(res_iter[0],2),
                                  user_id=current_user.id)
            db.session.add(new_ACdatum)
            db.session.commit()
            return redirect(url_for("views.actracker"))  # if user wants to save data, redirected to actracker page
        else:
            return render_template("aircalculator.html", user=current_user, display=1,
                                   results=[res_iter[0], sugg_iter[0], int(request.form.get("temp"))+round(sugg_iter[1],2)])  # if user does not want to save data, shows temporary results div
    return render_template("aircalculator.html", user=current_user, display=0)


@views.route('fancalculator', methods=['GET', 'POST'])
@login_required
def fancalculator():
    if request.method == 'POST':
        price = round(fan_price(inp('state'), inp('type'), inp('wattage'), inp('hours')), 1)
        if request.form.get("save") == "1":
            new_fanData = FanData(estimated_bill=price,
                                  user_id=current_user.id)
            db.session.add(new_fanData)
            db.session.commit()
            return redirect(url_for("views.actracker"))
        else:
            return render_template("fancalculator.html", user=current_user, display=1, bill=price)
    return render_template("fancalculator.html", user=current_user, display=0)


def is_empty(iter):
    return False if len(iter) > 0 else True


@views.route('actracker', methods = ['GET', 'POST'])
@login_required
def actracker():
    if request.method == "POST":
        current_user.state = current_user.state if request.form.get("state") == None else request.form.get("state")
        current_user.priority = current_user.priority if request.form.get("priority") == None else request.form.get("priority")
        current_user.budget = current_user.budget if request.form.get("goal_price") == "" else int(request.form.get("goal_price"))
        current_user.BTU_rating = current_user.BTU_rating if request.form.get("BTU_rating") == "" else request.form.get("BTU_rating")
        current_user.wattage =  current_user.wattage if request.form.get("wattage") == "" else request.form.get("wattage")
        current_user.size =  current_user.size if request.form.get("size") == None else request.form.get("size")
        current_user.typ =  current_user.typ if request.form.get("type") == None else request.form.get("type")
        flash('New account settings saved', category = 'success') 
    line_charts = [
        ["Entry " + str(label) for label in list(range(1,len(current_user.ACdata)+1))], #labels 
        [int(datum.temp) for datum in current_user.ACdata], #temperature data
        [int(datum.hours) for datum in current_user.ACdata], #hours data
        [float(datum.estimated_bill) for datum in current_user.ACdata], #estimated bill
        [float(datum.sugg_temp) for datum in current_user.ACdata], #suggested temperature data
        [float(datum.sugg_hours) for datum in current_user.ACdata] #suggested hour data
    ] # line chart
    return render_template("actracker.html", 
    user=current_user, 
    entry_count = len(current_user.ACdata), 
    chart1 = line_charts)

@views.route('about')
def about():
    return render_template("about.html",user=current_user)
