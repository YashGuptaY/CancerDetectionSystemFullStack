package com.ivanfranchin.doctorapi.mapper;

import com.ivanfranchin.doctorapi.model.User;
import com.ivanfranchin.doctorapi.rest.dto.UserDto;

import org.springframework.stereotype.Service;

@Service
public class UserMapperImpl implements UserMapper {

    @Override
    public UserDto toUserDto(User user) {
        if (user == null) {
            return null;
        }
        return new UserDto(user.getId(), user.getUsername(), user.getName(), user.getEmail(), user.getRole());
    }
}
