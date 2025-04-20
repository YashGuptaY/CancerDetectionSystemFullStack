package com.demo.bcs.mapper;

import com.demo.bcs.dto.UserDto;
import com.demo.bcs.model.User;

public interface UserMapper {

    UserDto toUserDto(User user);
}