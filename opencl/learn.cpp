#include <iostream>
#include <assert.h>
#include <string>

// Not defining this generates a compiler warning on g++
#define CL_TARGET_OPENCL_VERSION 120
#include "CL/cl.h"

using namespace std;

int main()
{
    cout << "Hello OpenCL!\n\n";

    cl_int err = 0;
    cl_platform_id platform_ids[5] = {0};
    cl_uint n_platforms = 0;
    err = clGetPlatformIDs(1, platform_ids, &n_platforms);
    if (err != CL_SUCCESS || n_platforms <= 0) {
        cerr << "Failed to find OpenCL platforms" << endl;
        return 1;
    }

    cout << "Found " << n_platforms << " OpenCL platforms:" << endl;
    cout << "=============================================" << endl;

    char info[1024] = {0};
    for (cl_uint i=0; i < n_platforms; ++i) {
        cl_platform_id id = platform_ids[i];
        size_t param_value_size = 0;

        err = clGetPlatformInfo(id, CL_PLATFORM_NAME, 1024, info, &param_value_size);
        cout << info << "\n";

        err = clGetPlatformInfo(id, CL_PLATFORM_VENDOR, 1024, info, &param_value_size);
        cout << info << "\n";

        err = clGetPlatformInfo(id, CL_PLATFORM_EXTENSIONS, 1024, info, &param_value_size);
        cout << info << "\n";

        err = clGetPlatformInfo(id, CL_PLATFORM_PROFILE, 1024, info, &param_value_size);
        cout << info << "\n";

        err = clGetPlatformInfo(id, CL_PLATFORM_VERSION, 1024, info, &param_value_size);
        cout << info << "\n";

        cout << "=============================================" << endl;
    }

    cl_platform_id plat_id = platform_ids[0];

    // Next, create an OpenCL context on the platform. Attempt to
    // create a GPU-based context, and if that fails, try to create
    // a CPU-based context.
    cl_context_properties context_props[] = {
        CL_CONTEXT_PLATFORM,
        (cl_context_properties)plat_id,
        0
    };

    cl_context context = clCreateContextFromType(context_props, CL_DEVICE_TYPE_GPU, NULL, NULL, &err);
    if (err != CL_SUCCESS) {
        cout << "Could not create GPU context, trying CPU..." << endl;
        context = clCreateContextFromType(context_props, CL_DEVICE_TYPE_CPU, NULL, NULL, &err);
        if (err != CL_SUCCESS) {
            cerr << "Could not create context" << endl;
            return 1;
        }
    }

    // Get context devices
    // First call to find out the buffer size needed to query devices in the context
    size_t param_value_size;
    err = clGetContextInfo(context, CL_CONTEXT_DEVICES, 0, NULL, &param_value_size);
    assert(err == CL_SUCCESS);
    assert(param_value_size > 0);
    size_t num_devices = param_value_size / sizeof(cl_device_id);
    assert(num_devices <= 50);
    cl_device_id devices[50] = {0};
    // Now get the actual info
    err = clGetContextInfo(context, CL_CONTEXT_DEVICES, 50*sizeof(cl_device_id), devices, NULL);
    if (err != CL_SUCCESS) {
        cerr << "Could not query devices from context" << endl;
        return 1;
    }
    cout << "Found " << num_devices << " device(s)\n";
    // There are like 40+ possible queries for devices using clGetDeviceInfo()
    // We are just picking the first one for convenience
    cl_device_id device = devices[0];

    // Create the command queue for device 0
    cl_command_queue command_queue = clCreateCommandQueue(context, device, 0, &err);
    assert(err == CL_SUCCESS);

    // Create program object
    string kernel_src = {
        "__kernel void hello_kernel(__global const float* a, __global const float* b, __global float* result)\n"
        "{\n"
        "    int g_id = get_global_id(0);\n"
        "    result[g_id] = a[g_id] + b[g_id];\n"
        "}\n"
    };
    const char* kernel_src_str = kernel_src.c_str();
    cl_program program = clCreateProgramWithSource(context, 1, (const char**)&kernel_src_str, NULL, &err);
    assert(err == CL_SUCCESS);
    assert(program != NULL);
    err = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
    if (err != CL_SUCCESS) {
        // Find out why compilation+link of program failed
        char log[16384];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        cerr << "Error building kernel: " << endl;
        cerr << log;
        clReleaseProgram(program);
        clReleaseCommandQueue(command_queue);
        clReleaseDevice(device);
        clReleaseContext(context);
        return 1;
    }

    // Create kernel object
    cl_kernel kernel = clCreateKernel(program, "hello_kernel", &err);
    assert(err == CL_SUCCESS);
    assert(kernel != NULL);

    // Create memory objects
    constexpr int ARRAY_SIZE = 1024;
    float a[ARRAY_SIZE];
    float b[ARRAY_SIZE];
    float result[ARRAY_SIZE];
    for (int i = 0; i < ARRAY_SIZE; ++i) {
        a[i] = (float)i;
        b[i] = (float)(2*i);
    }
    cl_mem mem_objects[3];
    mem_objects[0] = clCreateBuffer(context, CL_MEM_READ_ONLY|CL_MEM_COPY_HOST_PTR, ARRAY_SIZE*sizeof(float), a, &err);
    assert(err == CL_SUCCESS);
    assert(mem_objects[0] != NULL);
    mem_objects[1] = clCreateBuffer(context, CL_MEM_READ_ONLY|CL_MEM_COPY_HOST_PTR, ARRAY_SIZE*sizeof(float), b, &err);
    assert(err == CL_SUCCESS);
    assert(mem_objects[1] != NULL);
    mem_objects[2] = clCreateBuffer(context, CL_MEM_READ_WRITE, ARRAY_SIZE*sizeof(float), NULL, &err);
    assert(err == CL_SUCCESS);
    assert(mem_objects[2] != NULL);

    // Set kernel arguments (0,1,2) -> (a,b,result)
    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mem_objects[0]);
    assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 1, sizeof(cl_mem), &mem_objects[1]);
    assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 2, sizeof(cl_mem), &mem_objects[2]);
    assert(err == CL_SUCCESS);

    // Finally enqueue the kernel to be processed.
    size_t global_work_size = ARRAY_SIZE;
    size_t local_work_size = 1;
    err = clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL, &global_work_size, &local_work_size, 0, NULL, NULL);
    assert(err == CL_SUCCESS);

    // Read back the results
    // Block so that clEnqueueReadBuffer only returns once the read is complete
    cl_bool blocking = CL_TRUE;
    err = clEnqueueReadBuffer(command_queue, mem_objects[2], blocking, 0, ARRAY_SIZE*sizeof(float), result, 0, NULL, NULL);
    assert(err == CL_SUCCESS);

    // Output buffer result
    cout << "Results: \n";
    cout << "a = [" << a[0] << ", " << a[1] << ", " << a[2] << ", ...]" << endl;
    cout << "b = [" << b[0] << ", " << b[1] << ", " << b[2] << ", ...]" << endl;
    cout << "res = [" << result[0] << ", " << result[1] << ", " << result[2] << ", ...]" << endl;

    // cleanup
    clReleaseMemObject(mem_objects[0]);
    clReleaseMemObject(mem_objects[1]);
    clReleaseMemObject(mem_objects[2]);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(command_queue);
    clReleaseDevice(device);
    clReleaseContext(context);

}
