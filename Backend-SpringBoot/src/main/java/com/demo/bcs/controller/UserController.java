package com.demo.bcs.controller;

import com.demo.bcs.dto.UserDto;
import com.demo.bcs.mapper.UserMapper;
import com.demo.bcs.model.User;
import com.demo.bcs.security.CustomUserDetails;
import com.demo.bcs.security.service.UserService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import static com.demo.bcs.config.SwaggerConfig.BEARER_KEY_SECURITY_SCHEME;

import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @Operation(security = {@SecurityRequirement(name = BEARER_KEY_SECURITY_SCHEME)})
    @GetMapping("/me")
    public UserDto getCurrentUser(@AuthenticationPrincipal CustomUserDetails currentUser) {
        User user = userService.validateAndGetUserByUsername(currentUser.getUsername());
        return userMapper.toUserDto(user);
    }

    @Operation(security = {@SecurityRequirement(name = BEARER_KEY_SECURITY_SCHEME)})
    @GetMapping
    public List<UserDto> getUsers() {
        return userService.getUsers().stream()
                .map(userMapper::toUserDto)
                .collect(Collectors.toList());
    }

    @Operation(security = {@SecurityRequirement(name = BEARER_KEY_SECURITY_SCHEME)})
    @GetMapping("/{username}")
    public UserDto getUser(@PathVariable String username) {
        return userMapper.toUserDto(userService.validateAndGetUserByUsername(username));
    }

    @Operation(security = {@SecurityRequirement(name = BEARER_KEY_SECURITY_SCHEME)})
    @DeleteMapping("/{username}")
    public UserDto deleteUser(@PathVariable String username) {
        User user = userService.validateAndGetUserByUsername(username);
        userService.deleteUser(user);
        return userMapper.toUserDto(user);
    }
}
