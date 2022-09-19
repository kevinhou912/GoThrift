import re
import uuid
import random

locations = [
    [30.29128, -97.73858],
    [30.25768, -97.73870],
    [30.24638, -97.73780],
    [30.57844, -97.73786],
    [30.89765, -97.74577],
    [30.78654, -97.76748],
    [30.35475, -97.74748],
    [30.50833, -97.67895],
    [30.46578, -97.86954],
    [30.67843, -97.46558],
    [30.56473, -97.68695],
    [30.24263, -97.57586],
    [30.65732, -97.86954],
    [30.25347, -97.86869],
    [30.57489, -97.69685],
    [30.57833, -97.67849],
    [30.47558, -97.68484],
    [30.59557, -97.29485],
    [30.23151, -97.09685],
    [30.14253, -97.47578],
    [30.24353, -97.57589],
    [31.59557, -98.29485],
    [31.46578, -98.58574],
    [31.14253, -98.47578],
    [31.24353, -98.57589],
    [31.46578, -97.86954],
    [31.67843, -97.46558],
    [31.56473, -97.68695],
    [31.24263, -97.57586],
    [31.65732, -97.86954],
    [31.25347, -97.86869],
    [30.29128, -97.73858],
    [30.13645, -97.65758],
    [30.45362, -97.27364],
    [30.13243, -97.35342],
    [30.24251, -97.34241],
    [30.34252, -97.34252],
    [30.35254, -97.35342],
    [30.24356, -97.34252],
    [30.43345, -97.35353],
    [30.34362, -97.34464]
]
def submit_theme_request(request_form, image_storage):
    userdata = dict(request_form.form)
    id = str(uuid.uuid1())
    location = userdata["location"]
    description = userdata["description"]
    theme_image_name = id

    # Store image while creating new theme
    user_image = request_form.files['upload']
    id_token = request_form.cookies.get("token")
    if user_image:
        image_storage.child('/Theme/' + theme_image_name + '.jpg').put(user_image)
        theme_image_url = image_storage.child('/Theme/' + theme_image_name + '.jpg').get_url(id_token)
    else:
        theme_image_name = 'No_Image'
        theme_image_url = image_storage.child('/NoImage/NoImage.png').get_url(id_token)

    data = {"id": id, "location": location, "description": description,
            "theme_image_name": theme_image_name, "theme_image_url": theme_image_url}
    return data


def submit_report_request(request_form, image_storage,all_themes):
    userdata = dict(request_form.form)
    id = str(uuid.uuid1())
    store_name = userdata["store_name"]
    store_description = userdata["store_description"]
    store_tag = userdata["store_tag"]
    report_image_name = id

    # Store image while creating new report
    report_image = request_form.files['upload']
    id_token = request_form.cookies.get("token")
    if report_image:
        image_storage.child('/Report/' + report_image_name + '.jpg').put(report_image)
        report_image_url = image_storage.child('/Report/' + report_image_name + '.jpg').get_url(id_token)
    else:
        report_image_name = 'No_Image'
        report_image_url = image_storage.child('/NoImage/NoImage.png').get_url(id_token)

    # removed space and duplicates
    tags = list(set(store_tag.replace(" ", "").lower().split(",")))
    theme_id = userdata["Theme_list"]
    if all_themes:
        for theme in all_themes:
            if all_themes[theme]['id'] == theme_id:
                theme_name = all_themes[theme]['location']

    pickRandomLocation = random.sample(locations,1)
    print("Chetnaaaaaaaa")
    print(pickRandomLocation)
    data = {'id': id, "store_name": store_name, "description": store_description, "store_tag": tags,
            "theme_id": theme_id,
            'theme': theme_name, "report_image_name": report_image_name, "report_image_url": report_image_url,
            'gpslat':pickRandomLocation[0][0], 'gpslong':pickRandomLocation[0][1]
            }
    return data


def subscribe_theme_request(request_form):
    userdata = dict(request_form.form)
    id = userdata["id"]
    location = userdata["location"]
    description = userdata["description"]

    data = {"id": id,"location": location, "description": description}
    return data


def search_report_request(request_form, result_reports):
    result_search_report = {}
    if request_form.form['searchText']:
        tagsArray = re.split(",+", request_form.form['searchText'])
        for tag in tagsArray:
            current_tag = tag + '+'
            result_search_report = {}
            if result_reports:
                for report in result_reports:
                    search_results = re.findall(str(current_tag), "".join(result_reports[report]['store_tag']))
                    if search_results:
                        result_search_report.update({report: result_reports[report]})

    if not result_search_report:
        result_search_report['error'] = "No results matching your search."
    return result_search_report


def create_user_request(user_data):
    if 'email' in user_data:
        user_email = user_data['email']
    else:
        user_email = ''

    if 'name' in user_data:
        user_name = user_data['name']
    else:
        user_name = user_data['email'].split('@')[0]

    if not user_name:
        user_name = ''

    data = {"user_name": user_name, "user_email": user_email}
    return data


def get_user_subscribed_themes(all_themes, user_themes):
    subscribed_themes = {}
    unsubscribed_themes = {}
    if all_themes:
        if user_themes:
            for theme in all_themes:
                theme_is_subscribed = False
                for s_theme in user_themes:
                    if user_themes[s_theme]['id'] == all_themes[theme]['id']:
                        theme_is_subscribed = True
                        subscribed_themes[theme] = all_themes[theme]
                        break
                if not theme_is_subscribed:
                    unsubscribed_themes[theme] = all_themes[theme]
        else:
            subscribed_themes = {}
            unsubscribed_themes = all_themes

    if not subscribed_themes:
        subscribed_themes['error'] = 'You have not subscribed to any themes.'

    if not unsubscribed_themes:
        unsubscribed_themes['error'] = 'No themes are available.'

    data = {"subscribed_themes": subscribed_themes, "unsubscribed_themes": unsubscribed_themes}
    return data


def get_reports(all_reports):
    reports = {}

    if not all_reports:
        reports['error'] = 'There are no existing posts.'
    else:
        reports = all_reports

    data = {"all_reports": reports}
    return data


def get_user_reports(all_reports, user_reports):
    reports = {}

    if all_reports:
        if user_reports:
            for report in all_reports:
                for user_report in user_reports:
                    if user_reports[user_report]['id'] == all_reports[report]['id']:
                        reports[report] = all_reports[report]
                        break

    if not reports:
        reports['error'] = 'You have not created any posts yet.'

    data = {"user_reports": reports}
    return data


def get_all_themes(themes):
    all_themes = {}

    if not themes:
        all_themes[
            'error'] = 'There are no existing themes. You cannot create a post. Please create a theme first.'
    else:
        all_themes = themes

    data = {"all_themes": all_themes}
    return data

def unsubscribe_theme_request(request, user_themes,key):
    key_for_unsubscribed_theme = key
    if user_themes:
        for theme in user_themes:
            if user_themes[theme]['id'] == request.form['id']:
                key_for_unsubscribed_theme = theme
                break

    return key_for_unsubscribed_theme


def get_locations(all_reports):
    all_locations = []
    if all_reports:
        for report in all_reports:
            location = {}
            location['lat'] = all_reports[report]['gpslat']
            location['long'] = all_reports[report]['gpslong']
            location['name'] = all_reports[report]['store_name']
            location['image'] = all_reports[report]['report_image_url']
            all_locations.append(location)

    return all_locations

