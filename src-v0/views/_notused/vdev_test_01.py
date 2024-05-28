# ******************************************************************************
def test_test(input_param):
    import random
    import time
    rand_sleep = random.randint(2, 5)
    zzz_print("    %-28s: %s, rand_sleep %s" % ("test_test START", input_param, rand_sleep))
    time.sleep(rand_sleep)
    zzz_print("    %-28s: %s" % ("test_test END", input_param))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_testingview"}))
def vdev_testingview(request):
    viewname    = "vdev_testingview"
    zzz_print("    %-28s: %s" % ("viewname START", viewname))

    # TESTING THREADING
    from threading import Thread
    thread = Thread(target = test_test, args = ("a", ))
    thread.start()
    thread = Thread(target = test_test, args = ("b", ))
    thread.start()
    thread = Thread(target = test_test, args = ("c", ))
    thread.start()

    zzz_print("    %-28s: %s" % ("viewname END", viewname))
    return HttpResponseRedirect(reverse('vdev_home'))











































