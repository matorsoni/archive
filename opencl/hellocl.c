#include <stdio.h>
#include <assert.h>

#define CL_TARGET_OPENCL_VERSION 120
#include <CL/cl.h>

#define MAX_NUM_PLATFORMS 5
#define ARRAY_SIZE 1024

int main(int argc, char** argv) {
    cl_int err;

    // first get number of available platforms, then fill a buffer with their ids
    cl_uint num_platforms;
    err = clGetPlatformIDs(0, NULL, &num_platforms); assert(err == CL_SUCCESS);
    printf("Platforms found: %d\n\n", num_platforms);
    cl_platform_id plat_ids[MAX_NUM_PLATFORMS] = {};
    err = clGetPlatformIDs(num_platforms, plat_ids, NULL); assert(err == CL_SUCCESS);

    // query platform infos
    for (cl_uint i = 0; i < num_platforms; i++) {
        char info[2048] = {0};

        err = clGetPlatformInfo(plat_ids[i], CL_PLATFORM_NAME, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetPlatformInfo(plat_ids[i], CL_PLATFORM_VERSION, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetPlatformInfo(plat_ids[i], CL_PLATFORM_VENDOR, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetPlatformInfo(plat_ids[i], CL_PLATFORM_PROFILE, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetPlatformInfo(plat_ids[i], CL_PLATFORM_EXTENSIONS, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        printf("\n");
    }

    cl_platform_id platform = plat_ids[0];

    // query devices in the platform
    cl_uint num_devices;
    cl_device_id device_ids[5];
    // CL_DEVICE_TYPE_ALL, CL_DEVICE_TYPE_CPU, CL_DEVICE_TYPE_GPU,
    // CL_DEVICE_TYPE_DEFAULT, CL_DEVICE_TYPE_CUSTOM, CL_DEVICE_TYPE_ACCELERATOR
    cl_device_type device_type = CL_DEVICE_TYPE_ALL;
    err = clGetDeviceIDs(platform, device_type, 5, device_ids, &num_devices); assert(err == CL_SUCCESS);
    printf("Devices found: %d\n\n", num_devices);

    // print devices info
    for (cl_uint i = 0; i < num_devices; i++) {
        char info[2048] = {0};
        cl_uint number;
        cl_ulong mem;

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_NAME, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_VENDOR, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_VERSION, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_PROFILE, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DRIVER_VERSION, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_OPENCL_C_VERSION, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_EXTENSIONS, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(cl_uint), &number, NULL); assert(err == CL_SUCCESS);
        printf("CL_DEVICE_MAX_COMPUTE_UNITS: %d\n", number);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(cl_ulong), &mem, NULL); assert(err == CL_SUCCESS);
        printf("CL_DEVICE_GLOBAL_MEM_SIZE (bytes): %ld\n", mem);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_LOCAL_MEM_SIZE, sizeof(cl_ulong), &mem, NULL); assert(err == CL_SUCCESS);
        printf("CL_DEVICE_LOCAL_MEM_SIZE (bytes): %ld\n", mem);

        printf("\n");
    }

    // Create GPU context from platform
    cl_context_properties context_properties[] = {
        CL_CONTEXT_PLATFORM,
        (cl_context_properties)platform,
        0
    };
    cl_context context = clCreateContextFromType(context_properties, CL_DEVICE_TYPE_GPU, NULL, NULL, &err); assert(err == CL_SUCCESS);

    // print context info
    cl_uint context_ref_count;
    cl_uint context_num_devices;
    cl_device_id context_devices[16];
    err = clGetContextInfo(context, CL_CONTEXT_REFERENCE_COUNT, sizeof(cl_uint), &context_ref_count, NULL); assert(err == CL_SUCCESS);
    printf("CL_CONTEXT_REFERENCE_COUNT: %d\n", context_ref_count);

    err = clGetContextInfo(context, CL_CONTEXT_NUM_DEVICES, sizeof(cl_uint), &context_num_devices, NULL); assert(err == CL_SUCCESS);
    printf("CL_CONTEXT_NUM_DEVICES: %d\n", context_num_devices);

    err = clGetContextInfo(context, CL_CONTEXT_DEVICES, sizeof(context_devices), context_devices, NULL); assert(err == CL_SUCCESS);
    for (int i = 0; i < context_num_devices; i++) {
        char info[2048] = {0};
        err = clGetDeviceInfo(context_devices[i], CL_DEVICE_NAME, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);
    }

    // create command queue for a chosen device
    cl_device_id device = context_devices[0];
    cl_command_queue queue = clCreateCommandQueue(context, device, 0, &err); assert(err == CL_SUCCESS);

    // create program object and build its source, checking for compile errors
    const char* src =
        "__kernel void hello_kernel(__global const float* a, __global const float* b, __global float* c) {\n"
        "   int gid = get_global_id(0);\n"
        "   c[gid] = a[gid] + b[gid];\n"
        "}\n";
    cl_program program = clCreateProgramWithSource(context, 1, &src, NULL, &err); assert(err == CL_SUCCESS);
    err = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
    if (err != CL_SUCCESS) {
        char log[4096];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        printf("Program build log: %s\n", log);
    }

    // create kernel object
    cl_kernel kernel = clCreateKernel(program, "hello_kernel", &err); assert(err == CL_SUCCESS);

    // create memory objects
    float a[ARRAY_SIZE];
    float b[ARRAY_SIZE];
    float c[ARRAY_SIZE] = {0};
    for (int i=0; i < ARRAY_SIZE; i++) {
        a[i] = (float)i;
        b[i] = (float)(2 * i);
    }
    printf("Input values:\na = [%f, %f, %f, ...]\nb = [%f, %f, %f, ...]\n", a[0], a[1], a[2], b[0], b[1], b[2]);
    cl_mem mem_objects[3];
    mem_objects[0] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(a), a, &err); assert(err == CL_SUCCESS);
    mem_objects[1] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(b), b, &err); assert(err == CL_SUCCESS);
    mem_objects[2] = clCreateBuffer(context, CL_MEM_READ_WRITE, sizeof(c), NULL, &err); assert(err == CL_SUCCESS);

    // set kernel args
    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mem_objects[0]); assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 1, sizeof(cl_mem), &mem_objects[1]); assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 2, sizeof(cl_mem), &mem_objects[2]); assert(err == CL_SUCCESS);

    // enqueue kernel
    size_t global_work_size[1] = { ARRAY_SIZE };
    size_t local_work_size[1] = { 1 };
    err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, global_work_size, local_work_size, 0, NULL, NULL); assert(err == CL_SUCCESS);

    // read output
    err = clEnqueueReadBuffer(queue, mem_objects[2], CL_TRUE, 0, ARRAY_SIZE * sizeof(float), c, 0, NULL, NULL);
    printf("Output values:\nc = [%f, %f, %f, ...]\n", c[0], c[1], c[2]);

    return 0;
}
