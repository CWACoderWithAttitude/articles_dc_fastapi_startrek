package com.example.spring_boot_postgresql_crud.service;

import java.util.List;
import java.util.Optional;

import com.example.spring_boot_postgresql_crud.model.RoADTO;

public interface RoAService {

    RoADTO saveRoA(RoADTO ruleOfAqcuisition);

    List<RoADTO> getAllRulesOfAqcuisition();

    void deleteRuleOfAcquisition(Long id);
    /*
     * 
     * Optional<RoADTO> getRuletById(Long id);
     * 
     * 
     * 
     * RoADTO updateRoA(Long id, RoADTO ruleOfAqcuisition);
     * 
     */

}
