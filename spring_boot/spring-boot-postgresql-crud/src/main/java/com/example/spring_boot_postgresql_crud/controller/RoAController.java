package com.example.spring_boot_postgresql_crud.controller;

import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.tomcat.util.json.JSONParser;
import org.apache.tomcat.util.json.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource; // Add this import
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.spring_boot_postgresql_crud.model.RoA;
import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.service.RoAService;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import jakarta.annotation.PostConstruct;

@RestController
@RequestMapping("/api/roa")
public class RoAController {
    private static final Logger logger = LoggerFactory.getLogger(RoAController.class);
    RoAService roaService;
    @Autowired
    MeterRegistry registry;

    private Gauge rulesCountGauge;

    @Value("classpath:rules_of_acquisiton.json")
    // @Value("classpath:roa.json")
    Resource resource; // = new ClassPathResource("rules_of_acquisiton.json");

    public RoAController(RoAService roaService) {
        this.roaService = roaService;
    }

    @PostMapping
    public RoADTO createRoAA(@RequestBody RoADTO roADTO) {

        RoADTO createROA = roaService.saveRoA(roADTO);
        // rulesCreatedCounter.increment(); // increment counter on creation

        return createROA;
    }

    @GetMapping()
    public List<RoADTO> getAllRulesOfAqcuisition() {
        return roaService.getAllRulesOfAqcuisition();
    }

    @PostConstruct
    private void updateRuleCounter() {
        rulesCountGauge = Gauge.builder("rules_count", roaService, s -> s.getAllRulesOfAqcuisition().size())
                .description("Current number of rules of acquisition")
                .register(registry);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteRule(@PathVariable Long id) {
        try {
            roaService.deleteRuleOfAcquisition(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
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

    /** Read rule seed data from Resource and sava each rule to DB */
    private void readSeedData() throws IOException, ParseException {
        logger.info("seed data file: {}", resource.getFilename());
        InputStream in = resource.getInputStream();
        String jsonString = new String(in.readAllBytes());
        // Object json = new JSONParser(jsonString).parse();
        ArrayList<Object> array = new JSONParser(jsonString).parseArray();
        logger.info("seed data contents: {}", array);
        array.forEach(item -> {
            RoADTO dto = mapJsonItem2DTO(item);
            roaService.saveRoA(dto);
        });
    }

    private RoADTO mapJsonItem2DTO(Object item) {
        @SuppressWarnings("unchecked")
        Map<String, Object> map = (Map<String, Object>) item;
        RoA r = buildRoAFromJSONItem(map);
        logger.info(">> Rule: {}", r);
        RoADTO dto = buildRoADTO(r);
        return dto;
    }

    private RoADTO buildRoADTO(RoA r) {
        RoADTO dto = new RoADTO(
                null,
                r.getRule(),
                r.getRuleNumber(),
                r.getComment());
        return dto;
    }

    private RoA buildRoAFromJSONItem(Map<String, Object> map) {
        RoA r = new RoA();
        r.setRule((String) map.get("rule"));
        BigInteger ruleNumber = (BigInteger) map.get("ruleNumber");
        r.setRuleNumber(ruleNumber.longValue());
        r.setComment((String) map.get("comment"));
        return r;
    }
}