import zipfile,os,re,itertools

def neighborhood(iterable):
    iterator = iter(iterable)
    prev_item = None
    current_item = next(iterator) # throws StopIteration if empty.
    for next_item in iterator:
        yield (prev_item, current_item, next_item)
        prev_item = current_item
        current_item = next_item

name='11.zip'
with zipfile.ZipFile(name) as z:
    for filename in z.namelist():
        if not os.path.isdir(filename):
            with z.open(filename) as f:
                for prev,item,next_ in neighborhood(f):
                    if re.findall ('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)false\r\n', item.decode("utf-8")):
                        print(prev)
                        print(item)
                        print(next_)
                        print('---------------------------------------------------------------------------------------')
                        None

