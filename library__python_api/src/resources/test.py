from bson.objectid import ObjectId
from datetime import datetime
from tes.api import API, DB
from tes.api.response import APIResponse


@API.get("/tags")
@API.login_required
def get_tags():
    args = API.request.args
    tags = DB().tag.find({ "_cls" : { "$exists" : False}}).skip(
        int(args.get('skip', '0'))).limit(30)

    return APIResponse.ok({'entries': list(tags)})


@API.get("/tags/<string:entry_id>")
@API.login_required
def get_tag(entry_id):
    if not ObjectId.is_valid(entry_id):
        return APIResponse.bad_request('invalid entry id')

    tag = DB().tag.find_one({'_id': ObjectId(entry_id)})
    if not tag:
        return APIResponse.not_found()

    return APIResponse.ok({'entry': tag})


@API.patch("/tags/<string:entry_id>")
@API.login_required
def update_tag(entry_id):
    if not ObjectId.is_valid(entry_id):
        return APIResponse.bad_request('invalid entry id')

    tag = DB().tag.find_one({'_id': ObjectId(entry_id)})
    if not tag:
        return APIResponse.not_found()

    changes = API.request.data
    if len(changes) == 0:
        return APIResponse.ok({'status': 'ok', 'entry': tag})

    changes['lastupdate'] = datetime.utcnow()

    DB().tag.update_one(
        {'_id': ObjectId(entry_id)},
        {"$set": changes}
    )

    tag = DB().tag.find_one({'_id': ObjectId(entry_id)})

    return APIResponse.ok({'status': 'ok', 'entry': tag})


@API.post("/tags")
@API.login_required
def create_tag():
    changes = API.request.data
    if len(changes) == 0:
        return APIResponse.bad_request('no data found')

    changes['create_date'] = datetime.utcnow()
    changes['lastupdate'] = datetime.utcnow()


    result = DB().tag.insert_one(changes)
    tag = DB().tag.find_one({'_id': ObjectId(result.inserted_id)})

    return APIResponse.ok({'status': 'ok', 'entry': tag})


@API.delete("/tags/<string:entry_id>")
@API.login_required
def delete_tag(entry_id):
    if not ObjectId.is_valid(entry_id):
        return APIResponse.bad_request('invalid entry id')

    result = DB().tag.delete_one({'_id': ObjectId(entry_id)})
    if result.deleted_count != 1:
        return APIResponse.bad_request(
            f'did not delete just one (deleted:{result.deleted_count})')

    return APIResponse.ok({'status': 'ok'})
