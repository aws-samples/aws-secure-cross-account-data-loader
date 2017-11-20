import json, requests, time, sys
 
 
def create_spark_session(master_dns, kind='spark'):
    host = 'http://' + master_dns + ':8998'
    data = {'kind': kind}
    headers = {'Content-Type': 'application/json'}
 
    response = requests.post(host + '/sessions', data=json.dumps(data), headers=headers)
    print(response.json())
 
    return response.headers
 
 
def wait_for_idle_session(master_dns, response_headers):
    # wait for the session to be idle or ready for job submission
    status = ''
    host = 'http://' + master_dns + ':8998'
    session_url = host + response_headers['location']
 
    while status != 'idle':
        time.sleep(3)
        status_response = requests.get(session_url, headers=response_headers)
        status = status_response.json()['state']
        print('Session status: ' + status)
 
    return session_url
 
 
def kill_spark_session(session_url):
    requests.delete(session_url, headers={'Content-Type': 'application/json'})
 
 
def submit_statement(session_url, statement_path):
    statements_url = session_url + '/statements'
    with open(statement_path, 'r') as f:
        code = f.read()
    data = {'code': code}
    response = requests.post(statements_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response.json())
 
    return response
 
 
def track_statement_progress(master_dns, response_headers):
    statement_status = ''
    host = 'http://' + master_dns + ':8998'
 
    while statement_status != 'available':
        statement_url = host + response_headers['location']
        statement_response = requests.get(statement_url, headers={'Content-Type': 'application/json'})
        statement_status = statement_response.json()['state']
        print('Statement status: ' + statement_status)
        if 'progress' in statement_response.json():
            print('Progress: ' + str(statement_response.json()['progress']))
        time.sleep(10)
 
    final_statement_status = statement_response.json()['output']['status']
    if final_statement_status == 'error':
        raise ValueError(final_statement_status)
    print('Final Statement Status: ' + final_statement_status)
 
 
def main():
    cluster_dns = sys.argv[1]
    headers = create_spark_session(cluster_dns)
    session_url = wait_for_idle_session(cluster_dns, headers)
    statement_response = submit_statement(session_url, 'food_events.scala')
    track_statement_progress(cluster_dns, statement_response.headers)
    kill_spark_session(session_url)
 
 
if __name__ == '__main__':
    main(