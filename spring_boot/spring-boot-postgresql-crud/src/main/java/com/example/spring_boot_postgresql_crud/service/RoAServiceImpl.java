package com.example.spring_boot_postgresql_crud.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.example.spring_boot_postgresql_crud.model.RoA;
import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.repository.RoARepository;

@Service
public class RoAServiceImpl implements RoAService {

    private final RoARepository roaRepository;

    public RoAServiceImpl(RoARepository roaRepository) {
        this.roaRepository = roaRepository;
    }

    @Override
    public RoADTO saveRoA(RoADTO ruleOfAqcuisition) {
        RoA roa = convertToEntity(ruleOfAqcuisition);
        RoA savedRoA = roaRepository.save(roa);
        return convertToDTO(savedRoA);
    }

    @Override
    public List<RoADTO> getAllRulesOfAqcuisition() {
        return roaRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    // Convert RoA Entity to RoADTO
    private RoADTO convertToDTO(RoA roa) {
        return new RoADTO(roa.getId(), roa.getRule(), roa.getRuleNumber(), roa.getComment());
    }

    // Convert RoADTO to RoA Entity
    private RoA convertToEntity(RoADTO roaDTO) {
        RoA roa = new RoA();
        roa.setRule(roaDTO.rule());
        roa.setRuleNumber(roaDTO.ruleNumber());
        roa.setComment(roaDTO.comment());
        return roa;
    }

    @Override
    public void deleteRuleOfAcquisition(Long id) {
        roaRepository.deleteById(id);
    }

}