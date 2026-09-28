from backend.scripts.evaluate import check_case


def test_evaluation_recognizes_current_clarification_contract():
    assert check_case({'should_clarify': True}, {
        'intent': {'intent': 'database_query', 'needs_clarification': True},
    }) == (True, 'clarification_required')


def test_evaluation_recognizes_unsafe_requests():
    assert check_case({'expected_status': 'unsafe_request'}, {
        'intent': {'intent': 'unsafe_request'},
    }) == (True, 'unsafe_request')


def test_evaluation_does_not_pass_failed_database_execution():
    assert check_case({'expected_tables': ['shifts']}, {
        'intent': {'intent': 'database_query'}, 'retrieved_tables': ['shifts'], 'status': 'error',
    }) == (False, 'error')
