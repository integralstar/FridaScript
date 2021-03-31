import frida, sys

def on_message(message, data):
	print(message)

Hook_package = "com.dencreak.dlcalculator"

jscode = """
console.log("[+] Start Script");

Java.performNow(function () {
    const StringBuilder = Java.use('java.lang.StringBuilder');
    
    StringBuilder.toString.implementation = function () {
            var retVal = this.toString();
            console.log("StringBuilder.toString(): " + retVal);
            return retVal;
    };
});
"""

try:
    device = frida.get_usb_device(timeout=10)
    pid = device.spawn([Hook_package])
    print("App is starting... pid:{}".format(pid))                                 
    process = device.attach(pid)
    device.resume(pid)
    script = process.create_script(jscode)
    script.on('message', on_message)
    print('[+] Running Hook with Frida')
    script.load()
    sys.stdin.read()
 
except Exception as e:
    print(e)