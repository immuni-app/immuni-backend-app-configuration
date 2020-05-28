### Run the microservice

```bash
cd ./docker
docker-compose build
docker-compose up
```

The database is exposed on port 27017. You can add some example data running:
```python
from immuni_app_configuration.models.setting import Setting
from immuni_app_configuration.core.managers import managers
from immuni_common.enums import Platform
import asyncio

asyncio.run(managers.initialize())
# insert as many settings as needed
Setting(name="faq_url", platform=Platform.IOS, starting_build=1, value="https://faq.com").save()

asyncio.run(managers.cleanup())
```
