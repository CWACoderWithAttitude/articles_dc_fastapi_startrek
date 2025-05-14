package com.example.spring_boot_postgresql_crud.controller;

import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

import org.apache.tomcat.util.json.JSONParser;
import org.apache.tomcat.util.json.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource; // Add this import
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.spring_boot_postgresql_crud.model.RoA;
import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.service.RoAService;
import com.google.gson.JsonObject;

@RestController
@RequestMapping("/api/roa")
public class RoAController {
    private static final Logger logger = LoggerFactory.getLogger(RoAController.class);
    RoAService roaService;

    @Value("classpath:rules_of_acquisiton.json")
    // @Value("classpath:roa.json")
    Resource resource; // = new ClassPathResource("rules_of_acquisiton.json");

    public RoAController(RoAService roaService) {
        this.roaService = roaService;
    }

    private void readSeedData() throws IOException, ParseException {
        logger.info("seed data file: {}", resource.getFilename());
        InputStream in = resource.getInputStream();
        String jsonString = new String(in.readAllBytes());
        // Object json = new JSONParser(jsonString).parse();
        ArrayList<Object> array = new JSONParser(jsonString).parseArray();
        logger.info("seed data contents: {}", array);
        array.forEach(item -> {
            RoADTO dto = mapItem2DTO(item);
            roaService.saveRoA(dto);
        });
    }

    private RoADTO mapItem2DTO(Object item) {
        @SuppressWarnings("unchecked")
        java.util.Map<String, Object> map = (java.util.Map<String, Object>) item;
        RoA r = new RoA();
        r.setRule((String) map.get("rule"));
        BigInteger ruleNumber = (BigInteger) map.get("ruleNumber");
        r.setRuleNumber(ruleNumber.longValue());
        r.setComment((String) map.get("comment"));
        logger.info(">> Rule: {}", r);
        RoADTO dto = new RoADTO(
                null,
                r.getRule(),
                r.getRuleNumber(),
                r.getComment());
        return dto;
    }

    @PostMapping
    public RoADTO createRoAA(@RequestBody RoADTO roADTO) {
        return roaService.saveRoA(roADTO);
    }

    @GetMapping()
    public List<RoADTO> getAllRulesOfAqcuisition() {
        return roaService.getAllRulesOfAqcuisition();
    }

    @GetMapping("/seed")
    public ResponseEntity<String> seed() {
        try {
            readSeedData();
        } catch (IOException e) {
            ResponseEntity.internalServerError().body("Error reading seed data: " + e.getMessage());
        } catch (ParseException e) {
            ResponseEntity.internalServerError().body("Error parsing seed data:" + e.getMessage());
        }
        return ResponseEntity.ok("Seed data loaded successfully");
    }
}