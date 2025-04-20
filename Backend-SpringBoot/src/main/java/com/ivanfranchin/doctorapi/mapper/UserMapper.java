package com.ivanfranchin.doctorapi.mapper;

import com.ivanfranchin.doctorapi.model.User;
import com.ivanfranchin.doctorapi.rest.dto.UserDto;

public interface UserMapper {

    UserDto toUserDto(User user);
}