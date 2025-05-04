#include <stdio.h>
#include <assert.h>

#define CL_TARGET_OPENCL_VERSION 120
#include <CL/cl.h>

#define MAX_NUM_PLATFORMS 5
#define ARRAY_SIZE 1024

#define input_width 8
#define input_height 8
#define mask_width 3
#define mask_height 3
#define output_width 6
#define output_height 6

void print_matrix(cl_uint* data, int width, int height) {
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            printf("%d, ", data[i*width + j]);
        }
        printf("\n");
    }
}

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

    cl_platform_id platform;
    cl_device_type type = CL_DEVICE_TYPE_CPU;
    cl_uint num_devices;
    cl_device_id device_ids[5];
    for (int i = 0; i < num_platforms; i++) {
        // query devices in the platform
        err = clGetDeviceIDs(plat_ids[i], CL_DEVICE_TYPE_CPU, 0, NULL, &num_devices);
        //assert(err == CL_SUCCESS);
        if (num_devices > 0) {
            printf("Devices found: %d\n\n", num_devices);
            platform = plat_ids[i];
            err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, num_devices, device_ids, NULL); assert(err == CL_SUCCESS);
            break;
        }
    }

    // print devices info
    for (cl_uint i = 0; i < num_devices; i++) {
        char info[2048] = {0};
        cl_device_type type;
        cl_uint number;
        cl_ulong mem;

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_NAME, 2048, info, NULL); assert(err == CL_SUCCESS);
        printf("%s\n", info);

        err = clGetDeviceInfo(device_ids[i], CL_DEVICE_TYPE, sizeof(cl_device_type), &type, NULL); assert(err == CL_SUCCESS);
        if (type == CL_DEVICE_TYPE_CPU) {
            printf("CL_DEVICE_TYPE: CL_DEVICE_TYPE_CPU\n");
        } else if (type == CL_DEVICE_TYPE_GPU) {
            printf("CL_DEVICE_TYPE: CL_DEVICE_TYPE_GPU\n");
        } else {
            printf("CL_DEVICE_TYPE: not GPU and not CPU\n");
        }

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
    cl_context context = clCreateContextFromType(context_properties, type, NULL, NULL, &err); assert(err == CL_SUCCESS);

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
        "__kernel void convolve(__global const uint* input, __global const uint* mask, __global uint* output, const uint input_width, const uint mask_width) {\n"
        "   const int x = get_global_id(0);\n"
        "   const int y = get_global_id(1);\n"
        "   uint sum = 0;\n"
        "   for (int r = 0; r < mask_width; r++) {\n"
        "       const int idx = (y + r) * input_width + x;\n"
        "       for (int c = 0; c < mask_width; c++) {\n"
        "           sum += mask[r * mask_width + c] * input[idx + c];\n"
        "       }\n"
        "   }\n"
        "   output[y * get_global_size(0) + x] = sum;\n"
        "}\n";
    cl_program program = clCreateProgramWithSource(context, 1, &src, NULL, &err); assert(err == CL_SUCCESS);
    err = clBuildProgram(program, 0, NULL, NULL, NULL, NULL);
    if (err != CL_SUCCESS) {
        char log[4096];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        printf("Program build log: %s\n", log);
    }

    // create kernel object
    cl_kernel kernel = clCreateKernel(program, "convolve", &err); assert(err == CL_SUCCESS);

    // create memory objects
    cl_uint input[input_width * input_height] = {
        3, 1, 1, 4, 8, 2, 1, 3,
        4, 2, 1, 1, 2, 1, 2, 3,
        4, 4, 4, 4, 3, 2, 2, 2,
        9, 8, 3, 8, 9, 0, 0, 0,
        9, 3, 3, 9, 0, 0, 0, 0,
        0, 9, 0, 8, 0, 0, 0, 0,
        3, 0, 8, 8, 9, 4, 4, 4,
        5, 9, 8, 1, 8, 1, 1, 1
    };
    cl_uint mask[mask_width * mask_height] = {
        1, 1, 1,
        1, 0, 1,
        1, 1, 1
    };
    cl_uint output[output_width * output_height] = {0};
    printf("Input values:\n");
    print_matrix(input, input_width, input_height);
    printf("\nMask values:\n");
    print_matrix(mask, mask_width, mask_height);
    cl_mem mem_objects[3];
    mem_objects[0] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(input), input, &err); assert(err == CL_SUCCESS);
    mem_objects[1] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(mask), mask, &err); assert(err == CL_SUCCESS);
    mem_objects[2] = clCreateBuffer(context, CL_MEM_READ_WRITE, sizeof(output), NULL, &err); assert(err == CL_SUCCESS);

    // set kernel args
    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mem_objects[0]); assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 1, sizeof(cl_mem), &mem_objects[1]); assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 2, sizeof(cl_mem), &mem_objects[2]); assert(err == CL_SUCCESS);
    cl_uint ker_input_width = input_width;
    cl_uint ker_mask_width = mask_width;
    err = clSetKernelArg(kernel, 3, sizeof(cl_uint), &ker_input_width); assert(err == CL_SUCCESS);
    err = clSetKernelArg(kernel, 4, sizeof(cl_uint), &ker_mask_width); assert(err == CL_SUCCESS);

    // enqueue kernel
    size_t global_work_size[2] = { output_width, output_height };
    size_t local_work_size[2] = { 1, 1 };
    err = clEnqueueNDRangeKernel(queue, kernel, 2, NULL, global_work_size, local_work_size, 0, NULL, NULL); assert(err == CL_SUCCESS);

    // read output
    err = clEnqueueReadBuffer(queue, mem_objects[2], CL_TRUE, 0, output_width * output_height * sizeof(cl_uint), output, 0, NULL, NULL);
    printf("\nOutput values:\n");
    print_matrix(output, output_width, output_height);

    return 0;
}
