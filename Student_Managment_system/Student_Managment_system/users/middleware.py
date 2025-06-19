class SimpleLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code executed for each request before the view
        print(f"Request received: {request.method} {request.path}")
        
        # Pass request to the next middleware or view
        response = self.get_response(request)
        
        # Code executed for each response after the view
        print(f"Response status: {response.status_code}")
        
        return response
