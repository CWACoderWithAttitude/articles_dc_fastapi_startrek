package com.example.spring_boot_postgresql_crud.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.service.RoAService;

@RestController
@RequestMapping("/api/roa")
public class RoAController {
    RoAService roaService;

    public RoAController(RoAService roaService) {
        this.roaService = roaService;
    }

    @PostMapping
    public RoADTO createRoAA(@RequestBody RoADTO roADTO) {
        return roaService.saveRoA(roADTO);
    }

    @GetMapping
    public List<RoADTO> getAllRulesOfAqcuisition() {
        return roaService.getAllRulesOfAqcuisition();
    }
}