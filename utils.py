import sys
import logging
from copy import deepcopy


logger = logging.getLogger(__name__)


def aplus_json(course, index):
    '''
    Takes a dict and formats it to the form that aplus uses.
    @type course: C{class Course}
    @param course: an instance of a Course
    @type index: C{dict}
    @param index: updated contents of course and exercises (corresponding with the course instance)
    @rtype: C{dict}
    @return: an object representing the configuration file or None
    '''

    index_fields = ["name", "description", "lang", "contact", "assistants", "start",
                    "end", "categories", "numerate_ignoring_modules"]

    default_lang = course.get_def_lang()

    data = {}
    _copy_fields(data, index, index_fields)
    if "language" in index:
        data["lang"] = deepcopy(index["language"])

    def children_recursion(parent):
        if "children" not in parent:
            return []
        result = []
        for o in [o for o in parent["children"] if "key" in o]:
            of = _type_dict(o, index.get("exercise_types", {}))
            if "config" in of:
                of = _process_config_data(of, course, default_lang)
            of["children"] = children_recursion(o)
            result.append(of)
        return result

    modules = []
    if 'modules' in index:
        for m in index['modules']:
            mf = _type_dict(m, index.get("module_types", {}))
            mf["children"] = children_recursion(m)
            modules.append(mf)
    data["modules"] = modules

    # TODO "gitmanager?"
    # if "gitmanager" in settings.INSTALLED_APPS:
    #   data["build_log_url"] = request.build_absolute_uri(reverse("build-log-json", args=(course_key, )))
    return data


def _process_config_data(of, course, lang):
    exercises = course.get_exercise_keys()
    config_files = course.get_config_files()
    config_file = of.pop("config")
    exercise = {}
    new_data = {}
    if "key" in of and of["key"] in exercises:
        exercise = config_files[of["key"]]
        new_data.update(of)
        if exercise is None:
            return new_data

        if 'title' not in of and 'name' not in of:
            _copy_fields(new_data, exercise, ['title'])
        if 'description' not in of:
            new_data['description'] = exercise.get('description', '')

        form, i18n = form_fields(exercise, lang)
        print(of["key"])
        new_data['exercise_info'] = {
            'form_spec': form,
            'form_i18n': i18n,
        }

        if 'radar_info' in exercise:
            new_data['exercise_info']['radar'] = exercise['radar_info']

        if 'model_answer' in exercise:
            new_data['model_answer'] = exercise['model_answer']
        # TODO elif model_files  and elif createForm

        if 'exercise_template' in exercise:
            new_data['exercise_template'] = exercise['exercise_template']
        # TODO elif template_files

        return new_data

    else:
        logger.warning("Key not found: %s", of["key"])
        return of


def form_fields(exercise, lang):
    form = []
    i18n = {}

    def i18n_m(field):
        key = field
        if isinstance(field, dict):
            l, d = zip(*field.items())
            if lang in l:
                key = field[lang]
            else:
                key = d[0]
        elif not isinstance(field, str):
            print("???")

        while key in i18n and i18n[key] != field:
            print(key, field, "\n")
            logger.warning("Label should be unique, '%s' already exists in this exercise.", key)
            key += "_duplicate"
        i18n[key] = field
        return key

    def field_spec(f, n):
        field = {
            'key': f.get('key', 'field_' + str(n)),
            'type': f.get('type'),
            'title': f.get('title', ''),
            'required': f.get('required', False),
        }
        mods = f.get('compare_method', '').split('-')
        if 'int' in mods or 'float' in mods:
            field['type'] = 'number'

        if 'more' in f:
            field['description'] = i18n_m(f.get('more', ''))
        if 'more|i18n' in f:
            field['description'] = i18n_m(f.get('more|i18n', {}))

        if 'options' in f:
            title_map = {}
            enum = []
            m = 0
            for o in f.get('options', []):
                v = o.get('value', 'option_' + str(m))
                m += 1
                title_map[v] = i18n_m(o.get('label', o.get('label|i18n', '')))
                enum.append(v)
            field['titleMap'] = title_map
            field['enum'] = enum

        if 'extra_info' in f:
            extra = f.get('extra_info', '')
            for key in ['validationMessage']:
                if key in extra:
                    extra[key] = i18n_m(extra.get('key', ''))
            field.update(extra)
        if 'class' in field:
            field['htmlClass'] = field['class']
            del(field['class'])

        return field

    t = exercise.get("view_type", None)
    if t == 'access.types.stdsync.createForm':
        n = 0
        for fgs in exercise.get("fieldgroups", []):
            for fs in fgs.get('fields', []):
                t = fs.get('type', None)
                if t == 'table-radio' or t == 'table-checkbox':
                    logger.debug("Found 'table-radio'!")
                else:
                    form.append(field_spec(fs, n))
                    n += 1

    elif t == 'access.types.stdasync.acceptPost':
        for f in exercise.get('fields', []):
            form.append({
                'key': f.get('name'),
                'type': 'textarea',
                'title': i18n_m(f.get('title', '')),
                'required': f.get('required', False),
            })

    elif t == 'access.types.stdasync.acceptFiles':
        for f in exercise.get("files", []):
            form.append({
                'key': f.get('field', ''),
                'type': 'file',
                'title': i18n_m(f.get('name', {})),
                'required': f.get('required', True)
            })

    return form, i18n


def _copy_fields(result, dict_item, pick_fields):
    if dict_item is None:
        return
    for name in pick_fields:
        if name in dict_item:
            result[name] = deepcopy(dict_item[name])


def _type_dict(dict_item, dict_types):
    base = {}
    if "type" in dict_item and dict_item["type"] in dict_types:
        base = deepcopy(dict_types[dict_item["type"]])
    base.update(dict_item)
    if "type" in base:
        del base["type"]
    return base

# ----------------------------------------------------------------------------------------------------------------------


def error_print():
    return '{}. {}, line: {}'.format(sys.exc_info()[0],
                                     sys.exc_info()[1],
                                     sys.exc_info()[2].tb_lineno)




