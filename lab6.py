from flask import Blueprint, render_template, request, redirect, session, current_app

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    offices.append({'number': i, 'tenant': ''})


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    result = {
        'jsonrpc': '2.0',
        'id': id
    }
    
    if data['method'] == 'info':
        result['result'] = offices
        return result
    
    login = session.get('login')
    if not login:
        result['error'] = {
            'code': 1,
            'message': 'Unauthorized'
        }
        return result
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    result['error'] = {
                        'code': 2,
                        'message': 'Already booked'
                    }
                    return result
                office['tenant'] = login
                result['result'] = 'success'
                return result
        result['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }
        return result
    
    if data['method'] == 'cancel':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    result['error'] = {
                        'code': 3,
                        'message': 'Office not booked'
                    }
                    return result
                if office['tenant'] != login:
                    result['error'] = {
                        'code': 4,
                        'message': "You didn't book this office"
                    }
                    return result
                office['tenant'] = ''
                result['result'] = 'success'
                return result
        result['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }
        return result
    
    result['error'] = {
        'code': -32601,
        'message': 'Method not found'
    }
    return result