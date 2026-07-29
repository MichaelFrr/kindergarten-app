import datetime
from datetime import datetime, timedelta



now = datetime.now()
future_date = now + timedelta(days=30)

future_stamp = int(future_date.timestamp())
print(future_stamp)
