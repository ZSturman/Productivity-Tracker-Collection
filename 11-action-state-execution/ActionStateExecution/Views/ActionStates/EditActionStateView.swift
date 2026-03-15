//
//  EditActionStateView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/3/23.
//

import CoreData
import SwiftUI

struct EditActionStateView: View {
    @ObservedObject var actionState: ActionStateEntity
    let fieldVariableViewModel: FieldVariableViewModel
    
    @State private var showingSheet = false
    @State private var selectedField: FieldEntity? = nil
    @State private var fieldVariables: [FieldVariableEntity] = []
    @State var fieldToPass: InputFieldVariables? 

    
    @State private var name: String = ""
    @State private var category: String = ""
    @State private var explanation: String = ""
    @State private var collectDate: Bool = false
    @State private var collectLocation: Bool = false
    @State private var collectTime: Bool = false
    
   
    init(actionState: ActionStateEntity, context: NSManagedObjectContext) {
        self.actionState = actionState
        self.fieldVariableViewModel = FieldVariableViewModel(context: context)
    }

    var sortedFields: [FieldEntity] {
        let optionalFields = actionState.fields as? Set<FieldEntity>
        let fields = Array(optionalFields ?? [])
        return fields.sorted(by: { $0.order < $1.order })
    }

    var body: some View {
        Form {
            Section(header: Text("General Data")) {
                TextField("Name", text: $name)
                TextField("Category", text: $category)
                
                Text("Topic: \(actionState.topic?.name ?? "")")
            }
            
            Section(header: Text("Descriptors")) {
                TextField("Explanation", text: $explanation)
            }
            
            Section(header: Text("Collection Attributes")) {
                Toggle("Collect Date", isOn: $collectDate)
                Toggle("Collect Location", isOn: $collectLocation)
                Toggle("Collect Time", isOn: $collectTime)
            }
            
            ForEach(sortedFields, id: \.self) { field in
                Text("\(field.fieldName ?? "")")
                    .onTapGesture {
                        self.selectedField = field
                        
                        // Fetch the field variables for the selected field
                        self.fieldVariableViewModel.fetchFieldVariables(for: field)
                        
                        let textDefaultBoolVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "textDefaultBool" })?.value ?? "")
                        let textDefaultVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "textDefault" })?.value
                        
                        let countDirectionVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countDirection" })?.value
                               let countDecimalsVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countDecimals" })?.value ?? "")
                               let countNegativesVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countNegatives" })?.value ?? "")
                               let countCurrencyVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countCurrency" })?.value ?? "")
                               let countToVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countTo" })?.value ?? "")
                               let countToValueVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countToValue" })?.value
                               let countToResultVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countToResult" })?.value
                               let countToAlertBoolVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countToAlertBool" })?.value ?? "")
                               let countFromVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countFrom" })?.value ?? "")
                               let countFromValueVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "countFromValue" })?.value
                               let stepCountValueVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "stepCountValue" })?.value
                        
                        let boolDefaultVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "boolDefault" })?.value ?? "")
                               let numberDecimalsVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "numberDecimals" })?.value ?? "")
                               let numberNegativeVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "numberNegative" })?.value ?? "")
                               let numberCurrencyVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "numberCurrency" })?.value ?? "")
                               let numberDefaultVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "numberDefault" })?.value

                               let listSelectMultipleVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "listSelectMultiple" })?.value ?? "")
                               let listAddAtExecutionVar = Bool(self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "listAddAtExecution" })?.value ?? "")
                               let listSelectedListVar = UUID(uuidString: self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "listSelectedList" })?.value ?? "")

                               let uploadTypeVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "uploadType" })?.value
                               let captureTypeVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "captureType" })?.value
                               let otherTypeVar = self.fieldVariableViewModel.fieldVariables.first(where: { $0.variable == "otherType" })?.value


                        
                        // Prepare the field to pass
                        self.fieldToPass = InputFieldVariables(
                            name: field.fieldName ?? "",
                            prompt: field.prompt ?? "",
                            selection: field.fieldType ?? "",
                            
                            textDefaultBool: textDefaultBoolVar,
                            textDefault: textDefaultVar,
                            
                            countDirection: countDirectionVar,
                            countDecimals: countDecimalsVar,
                            countNegatives: countNegativesVar,
                            countCurrency: countCurrencyVar,
                            countTo: countToVar,
                            countToValue: countToValueVar,
                            countToResult: countToResultVar,
                            countToAlertBool: countToAlertBoolVar,
                            countFrom: countFromVar,
                            countFromValue: countFromValueVar,
                            stepCountValue: stepCountValueVar,
                            boolDefault: boolDefaultVar,
                            numberDecimals: numberDecimalsVar,
                            numberNegative: numberNegativeVar,
                            numberCurrency: numberCurrencyVar,
                            numberDefault: numberDefaultVar,
                            listSelectMultiple: listSelectMultipleVar,
                            listAddAtExecution: listAddAtExecutionVar,
                            listSelectedList: listSelectedListVar,
                            uploadType: uploadTypeVar,
                            captureType: captureTypeVar,
                            otherType: otherTypeVar
                        )
                        
                        // Show the sheet
                        self.showingSheet = true
                    }
            }



        }
        .sheet(isPresented: $showingSheet) {
            if let field = self.fieldToPass {
                let onFinish: (InputFieldVariables) -> Void = { updatedField in
                    // Update the FieldEntity instance with the updatedField data
                    self.selectedField?.fieldName = updatedField.name
                    self.selectedField?.prompt = updatedField.prompt
                    self.selectedField?.fieldType = updatedField.selection

                    // Update the corresponding FieldVariableEntity instances
                    self.fieldVariableViewModel.updateFieldVariable(for: self.selectedField, with: updatedField)

                    // Save the managed object context
                    do {
                        try self.selectedField?.managedObjectContext?.save()
                    } catch {
                        print("Failed to save changes: \(error)")
                    }

                    // Hide the sheet
                    self.showingSheet = false
                }

                EditInputFields(field: .constant(field), onFinish: onFinish)
            } else {
                // You can show an empty view or an error message here
                EmptyView()
            }
        }



        .navigationTitle("Edit Action State")
        .onAppear {
            // Initialize the state variables when the view appears
            self.name = actionState.name ?? ""
            self.category = actionState.category ?? ""
            self.explanation = actionState.explanation ?? ""
            self.collectDate = actionState.collectDate
            self.collectLocation = actionState.collectLocation
            self.collectTime = actionState.collectTime
        }
        .navigationBarItems(trailing: Button("Save") {
            // Update the actionState with the new values
            actionState.name = name
            actionState.category = category
            actionState.explanation = explanation
            actionState.collectDate = collectDate
            actionState.collectLocation = collectLocation
            actionState.collectTime = collectTime

            // Remember to save the context to persist changes
            do {
                try actionState.managedObjectContext?.save()
            } catch {
                print("Failed to save changes: \(error)")
            }
        })
    }
}
