def handle_form_errors(form):
	if form.errors:
		first_error_list = next(iter(form.errors.values()), None)
		if first_error_list:
			return first_error_list[0]
	return 'Unknown error. Try again.'
