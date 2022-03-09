const f_vector = [0,0,0]
const f_quat = [0,0,0,0]
export const initial_point = {
    // "ccno": 0,
    // "altitude": 1,
    // "linear_acc": 2,
    // "acc": 3,
    // "euler": 4,
    // "gyr": 5,
    // "quat": 6
    ccno:0,
    mm_mode:0,
    agl:0,
    altitude:0,
    linear_acc:f_vector,
    acc:f_vector,
    euler:f_vector,
    gyr:f_vector,
    quat:f_quat
  }

export function initial_point_from_cn(cn) {
    return {
    ccno:cn,
    mm_mode:0,
    agl:0,
    altitude:0,
    linear_acc:f_vector,
    acc:f_vector,
    euler:f_vector,
    gyr:f_vector,
    quat:f_quat
    }
}