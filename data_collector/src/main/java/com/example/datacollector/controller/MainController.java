package com.example.datacollector.controller;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.json.JSONObject;
import lombok.extern.slf4j.Slf4j;

@RestController
public class MainController {
    private static final String template = "Hello, %s!";

    private final AtomicInteger countRawData = new AtomicInteger(0);

    @GetMapping("/data")
    public String getData(@RequestParam(value = "name", defaultValue = "World") String name) {
        return String.format(template, name);
    }

    @PostMapping("/data")
    public ResponseEntity<String> postData(@RequestBody String body) throws IOException {
        Files.createDirectories(Paths.get("data"));
        // open a file named "data.txt"
        try (OutputStream os = new FileOutputStream("data/data" + countRawData +".txt", true)) {
            os.write(body.getBytes());
            countRawData.getAndIncrement();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        // return a http response with 200 status code
        return ResponseEntity.ok().build();
    }

    @PostMapping("/file")
    public ResponseEntity<String> postFile(@RequestParam("file") MultipartFile file) throws IOException {

        String fileName = StringUtils.cleanPath(Objects.requireNonNull(file.getOriginalFilename()));

        // creat the directory if it doesn't exist
        Files.createDirectories(Paths.get("file"));
        // create the file path
        Path filePath = Paths.get("file/" + fileName);

        // create the file if it doesn't exist
        if (!Files.exists(filePath)) {
            Files.createFile(filePath);
        }

        // save the file to the local directory
        Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

        return ResponseEntity.ok().build();
    }
}