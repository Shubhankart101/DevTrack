import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import (
    Reporter,
    Issue,
    CriticalIssue,
    LowPriorityIssue,
    REPORTERS_FILE,
    ISSUES_FILE,
    load_json_file,
    save_json_file,
)


def _find_by_id(records, record_id):
    for record in records:
        if record.get('id') == record_id:
            return record
    return None


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def get_issue(request):
    issue_id = _safe_int(request.GET.get('id'))
    if issue_id is None:
        return None

    issues = load_json_file(ISSUES_FILE)
    for issue in issues:
        if issue.get('id') == issue_id:
            return issue
    return JsonResponse({'error': 'Issue not found'}, status=404)


def api_root(request):
    return JsonResponse({
        'endpoints': [
            '/api/reporters/',
            '/api/reporters/?id=<id>',
            '/api/issues/',
            '/api/issues/?id=<id>',
            '/api/issues/?status=<status>',
        ]
    }, status=200)


def reporters_view(request):
    if request.method == 'GET':
        reporters = load_json_file(REPORTERS_FILE)
        reporter_id_param = request.GET.get('id')
        reporter_id = _safe_int(reporter_id_param)
        if reporter_id_param is not None and reporter_id is None:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        if reporter_id is not None:
            reporter = _find_by_id(reporters, reporter_id)
            if not reporter:
                return JsonResponse({'error': 'Reporter not found'}, status=404)
            return JsonResponse(reporter, status=200)
        return JsonResponse(reporters, safe=False, status=200)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if not isinstance(data, dict):
            return JsonResponse({'error': 'JSON object required'}, status=400)

        reporter = Reporter(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            team=data.get('team'),
        )
        try:
            reporter.validate()
        except ValueError as exc:
            return JsonResponse({'error': str(exc)}, status=400)

        reporters = load_json_file(REPORTERS_FILE)
        if _find_by_id(reporters, reporter.id):
            return JsonResponse({'error': 'Reporter with this ID already exists'}, status=400)

        reporters.append(reporter.to_dict())
        save_json_file(REPORTERS_FILE, reporters)
        return JsonResponse(reporter.to_dict(), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def issues_view(request):
    if request.method == 'GET':
        issue_id_param = request.GET.get('id')
        issue_id = _safe_int(issue_id_param)
        if issue_id_param is not None and issue_id is None:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        status_filter = request.GET.get('status')
        if issue_id is not None:
            issue = get_issue(request)
            if isinstance(issue, JsonResponse):
                return issue
            return JsonResponse(issue, status=200)

        issues = load_json_file(ISSUES_FILE)
        if status_filter:
            filtered = [issue for issue in issues if issue.get('status') == status_filter]
            return JsonResponse(filtered, safe=False, status=200)
        return JsonResponse(issues, safe=False, status=200)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if not isinstance(data, dict):
            return JsonResponse({'error': 'JSON object required'}, status=400)

        priority = data.get('priority')
        issue_cls = Issue
        if priority == 'critical':
            issue_cls = CriticalIssue
        elif priority == 'low':
            issue_cls = LowPriorityIssue

        issue = issue_cls(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority=data.get('priority'),
            reporter_id=data.get('reporter_id'),
        )

        try:
            issue.validate()
        except ValueError as exc:
            return JsonResponse({'error': str(exc)}, status=400)

        issues = load_json_file(ISSUES_FILE)
        if _find_by_id(issues, issue.id):
            return JsonResponse({'error': 'Issue with this ID already exists'}, status=400)

        # ensure reporter exists
        reporters = load_json_file(REPORTERS_FILE)
        if not _find_by_id(reporters, issue.reporter_id):
            return JsonResponse({'error': 'Reporter not found'}, status=400)

        response_data = issue.to_dict()
        response_data['message'] = issue.describe()
        issues.append(response_data)
        save_json_file(ISSUES_FILE, issues)
        return JsonResponse(response_data, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
