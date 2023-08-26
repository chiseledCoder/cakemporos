


  # @classmethod
  #   def get_total_count_by_day(cls, user, days):
  #       now = datetime.now(tz=user.settings.time_zone).date()

  #       glucose_averages = Glucose.objects.avg_by_day((now - timedelta(days=days)), now, user)

  #       data = {'dates': [], 'values': []}
  #       for avg in glucose_averages:
  #           rounded_value = core_utils.round_value(avg['avg_value'])
  #           data['values'].append(core_utils.glucose_by_unit_setting(user, rounded_value))
  #           data['dates'].append(avg['record_date'].strftime('%m/%d'))

  #       return data

