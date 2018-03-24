# settings
A module used to read, store and edit settings.
# Example
### Example usage of new()(Depricated):
```python
import settings as s
s.new('hello.cfg')
s.asetting = 'value'
if not s.exists('somesetting'):
    s.somesetting = 'something'
s.update()
```
### Example usage of load():
```python
import settings
s = settings.load('settingsfile.json')
s['setting'] = 'value'
s['alist'] = [1,2,3,4]
if not s.exists('somesetting'):
    s['somesetting'] = 'something'
s.close()
```
