//
//  TempInputExecution.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import CoreData
import SwiftUI

struct TempInputExecution: Equatable, Hashable {
    var id: UUID
    
    var inputExecutionEntityName: InputExecutionEntityType
    var outputType: String {
        return inputExecutionEntityName.entityDataType
    }
    
    var inputID: UUID?
    var latitude: Double?
    var longitude: Double?
    
    var outputValueDatetime: Date?
    var outputValueNumber: Double?
    var outputValueString: String?
    
    var calculationInputID: UUID?
    var calculationOperation: String?
    var outputValueType: String?
    var valueOne: Double?
    var valueTwo: Double?
    

    
    init(id: UUID, inputExecutionType: InputExecutionEntityType) {
        self.id = id
        self.inputExecutionEntityName = inputExecutionType
    }
}

extension TempInputExecution {
    init?(id: UUID, outputType: String) {
        guard let inputExecutionType = InputExecutionEntityType.entityType(fromOutputType: outputType) else {
            return nil
        }
        
        self.init(id: id, inputExecutionType: inputExecutionType)
    }
}


enum InputExecutionEntityType: String, CaseIterable {
    case InputExecutionDatetime = "InputExecutionDatetime"
    case InputExecutionNumber = "InputExecutionNumber"
    case InputExecutionLocation = "InputExecutionLocation"
    case InputExecutionString = "InputExecutionString"
    case InputExecutionCalculation = "InputExecutionCalculation"
    
    var inputExecutionEntityName: String {
        return self.rawValue
    }
    
    var entityDataType: String {
        switch self {
        case .InputExecutionDatetime:
            return "Date"
        case .InputExecutionNumber:
            return "Double"
        case .InputExecutionLocation:
            return "Location"
        case .InputExecutionString:
            return "String"
        case .InputExecutionCalculation:
            return "Calculation"
        }
    }
}

extension InputExecutionEntityType {
    static func entityType(fromOutputType outputType: String) -> InputExecutionEntityType? {
        switch outputType {
        case "Date":
            return .InputExecutionDatetime
        case "Double":
            return .InputExecutionNumber
        case "Location":
            return .InputExecutionLocation
        case "String":
            return .InputExecutionString
        case "Calculation":
            return .InputExecutionCalculation
        default:
            return nil
        }
    }
}
// MARK: - Initializing TempInputExecution from InputExecution
extension TempInputExecution {
    init(from inputExecution: InputExecution) {
        self.id = inputExecution.id ?? UUID()
        self.inputExecutionEntityName = InputExecutionEntityType(rawValue: inputExecution.entity.name ?? "") ?? .InputExecutionString
        
        switch inputExecutionEntityName {
        case .InputExecutionDatetime:
            if let inputExecution = inputExecution as? InputExecutionDatetime {
                // Initialize properties specific to InputExecutionDatetime
                self.outputValueDatetime = inputExecution.outputValue
            }
        case .InputExecutionNumber:
            if let inputExecution = inputExecution as? InputExecutionNumber {
                // Initialize properties specific to InputExecutionNumber
                self.outputValueNumber = inputExecution.outputValue
            }
        // ... handle other cases ...
        default:
            break
        }
    }
}

// MARK: - Initializing InputExecution from TempInputExecution
extension InputExecution {
    static func create(from tempObject: TempInputExecution, in context: NSManagedObjectContext) -> InputExecution? {
        let entityName = tempObject.inputExecutionEntityName.inputExecutionEntityName
        guard let entity = NSEntityDescription.entity(forEntityName: entityName, in: context) else { return nil }
        let inputExecution = InputExecution(entity: entity, insertInto: context)
        
        inputExecution.id = tempObject.id
        
        switch tempObject.inputExecutionEntityName {
        case .InputExecutionDatetime:
            if let inputExecution = inputExecution as? InputExecutionDatetime {
                // Set properties specific to InputExecutionDatetime
                inputExecution.outputValue = tempObject.outputValueDatetime
            }
        case .InputExecutionNumber:
            if let inputExecution = inputExecution as? InputExecutionNumber {
                // Set properties specific to InputExecutionNumber
                inputExecution.outputValue = tempObject.outputValueNumber ?? 0
            }
        // ... handle other cases ...
        default:
            break
        }
        
        return inputExecution
    }
}
